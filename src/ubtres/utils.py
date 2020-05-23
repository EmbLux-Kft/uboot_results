from flask import current_app
from ubtres import db
from ubtres.models import Result
import json
import re

def get_defconfig_data(defconfig, count, uid=None):
    result = Result.query.filter(Result.defconfig==defconfig).all()

    if result == None:
        return None, None

    i = 0
    ids = []
    dates = []
    images = []
    for res in reversed(result):
        if uid != None:
            if res.id > uid:
                continue
        d = res.to_dict()
        ids.insert(0, res.id)
        dates.insert(0, d["basecommit"])
        images.insert(0, d["images"])
        i += 1
        if i == count:
            return ids, dates, images

    return ids, dates, images

def get_images_names(images):
    names = []
    for img in images:
        js_string = json.loads(img)
        for n in js_string:
            if n["name"] not in names:
                names.append(n["name"])

    return names

def get_images_value(img, name):
    """
    search in img if name is found
    if so, return value
    else -1
    """
    js_string = json.loads(img)
    for n in js_string:
        if n["name"] == name:
            return int(n["size"])
    return -1

def convert_images_to_picture(images):
    names = get_images_names(images)
    pic = []
    # search for all names
    for n in names:
        values = []
        for img in images:
            values.append(get_images_value(img, n))
        pic.append({"name":n, "values":values})

    return pic

def systemmap_to_dict(filename):
    d = []
    with open(filename) as f:
        for line in f:
            if line[0] == "#":
                continue

            (addr, typ, name) = line.split()
            # ignore BSS
            #if "B" in typ.upper():
            #    continue
            exists = False
            for o in d:
                if o["name"] == name:
                    exists = True
                    break
            if exists:
                # in already existing ???
                pass
                #print("Found doubled entry ", name)
            else:
                d.append({"addr":addr, "typ":typ.upper(), "name":name})
    return d

# get size of each entry
# if next item is not same type, set to 0
# b, B, A
# t, T, W, r, R, d, D
#
# if same address next item until address different
#    all values same length
def systemmap_get_calc_sizes(d):
    old = None
    fixes = []
    for n in d:
        newaddr = int(n["addr"], 16)
        if old == None:
            old = n
            continue
        old["size"] = newaddr - int(old["addr"], 16)
        # get size later
        if old["size"] == 0:
            fixes.append(old)
        else:
            if len(fixes) != 0:
                for f in fixes:
                    f["size"] = old["size"]
                fixes = []
        old = n

#########
# code from linux:/scripts/bload-o-meter
re_NUMBER = re.compile(r'\.[0-9]+')

def getsizes(file, format):
    sym = {}
    sizes = systemmap_to_dict(file)
    systemmap_get_calc_sizes(sizes)
    for s in sizes:
        try:
            size = s["size"]
        except:
            continue
        name = s["name"]
        typ = s["typ"]

        if typ in format:
            # strip generated symbols
            if name.startswith("__mod_"): continue
            if name.startswith("__se_sys"): continue
            if name.startswith("__se_compat_sys"): continue
            if name.startswith("__addressable_"): continue
            if name == "linux_banner": continue
            # statics and some other optimizations adds random .NUMBER
            name = re_NUMBER.sub('', name)
            ns = sym.get(name)
            if ns == None:
                sym[name] = int(size)
            else:
                sym[name] = ns + int(size)

    return sym

def calc(oldfile, newfile, format):
    old = getsizes(oldfile, format)
    new = getsizes(newfile, format)
    grow, shrink, add, remove, up, down = 0, 0, 0, 0, 0, 0
    delta, common = [], {}
    otot, ntot = 0, 0

    for a in old:
        if a in new:
            common[a] = 1

    for name in old:
        otot += old[name]
        if name not in common:
            remove += 1
            down += old[name]
            delta.append((-old[name], name))

    for name in new:
        ntot += new[name]
        if name not in common:
            add += 1
            up += new[name]
            delta.append((new[name], name))

    for name in common:
        d = new.get(name, 0) - old.get(name, 0)
        if d>0: grow, up = grow+1, up+d
        if d<0: shrink, down = shrink+1, down-d
        delta.append((d, name))

    delta.sort()
    delta.reverse()
    return grow, shrink, add, remove, up, down, delta, old, new, otot, ntot

def print_result(oldfile, newfile, symboltype, symbolformat):
    grow, shrink, add, remove, up, down, delta, old, new, otot, ntot = \
    calc(oldfile, newfile, symbolformat)

    print("add/remove: %s/%s grow/shrink: %s/%s up/down: %s/%s (%s)" % \
          (add, remove, grow, shrink, up, -down, up-down))
    print("%-40s %7s %7s %+7s" % (symboltype, "old", "new", "delta"))
    diffs = []
    for d, n in delta:
        if d:
            print("%-40s %7s %7s %+7d" % (n, old.get(n,"-"), new.get(n,"-"), d))
            diffs.append({"name":n, "oldsize":old.get(n,"-"), "newsize":new.get(n,"-"), "delta":d})

    if otot:
        percent = (ntot - otot) * 100.0 / otot
    else:
        percent = 0
    print("Total: Before=%d, After=%d, chg %+.2f%%" % (otot, ntot, percent))

    return diffs

def diff_bloat_o_meter(oldfile, newfile):
    fd = print_result(oldfile, newfile, "Function", "tT")
    dd = print_result(oldfile, newfile, "Data", "dDbB")
    ro = print_result(oldfile, newfile, "RO Data", "rR")

    return fd, dd, ro

#########

def stats_get_diff_sizes(defconfig, count, uid=None):
    """
    get binary size changes from defconfig count times.

    return array if dictionary from form:
      [{
         "prevcommit":previouscommit,
         "commit":commit,
         "function":[{'name': 'fctname', 'oldsize': int, 'newsize': int, 'delta': int}]
         "data":[{'name': 'dataname', 'oldsize': int, 'newsize': int, 'delta': int}]
         "readonly":[{'name': 'ro data name', 'oldsize': int, 'newsize': int, 'delta': int}]
       },
      ]
    """
    count += 1
    ids, dates, images = get_defconfig_data(defconfig, count, uid)
    if dates == None:
        print("No dates")
        return None

    # shorten commit string to 6
    dates = [(d[:6] + '..') if len(d) > 6 else d for d in dates]

    print("IDS ", ids)
    if (len(ids) < 2):
            print(f"not enough data")
            return None

    # only print the last 2 commits
    if len(ids) > 3:
        ids = ids[len(ids) - 3:]
        dates = dates[len(dates) - 3:]
        images = images[len(images) - 3:]
    values = []
    i = 0
    for uid in ids:
        if i == 0:
            uidold = uid
            i += 1
            continue
        print("UID O ", uidold)
        print("UID N ", uid)
        path = current_app.config['STORE_FILES'] + f"/{uidold}"
        fnold = f"{path}/System.map"
        path = current_app.config['STORE_FILES'] + f"/{uid}"
        fnnew = f"{path}/System.map"
        print("PATH ", fnold, fnnew)
        try:
            fd, dd, ro = diff_bloat_o_meter(fnold, fnnew)
        except:
            print(f"not enough data file {fnold} {fnnew}")
            return None

        val = {"prevcommit":dates[i - 1], "commit":dates[i], "function":fd, "data":dd, "readonly":ro}
        values.append(val)
        i += 1
        uidold = uid

    print("VALUES ", values)
    for val in values:
        print("Commit ", val["commit"])
        print("Function")
        print(f"name                                            old        new       delta")
        diffs = val["function"]
        for d in diffs:
            print(f'{d["name"]:40} {d["oldsize"]:10} {d["newsize"]:10}  {d["delta"]:+10}')
        print("Data")
        print(f"name                                            old        new       delta")
        diffs = val["data"]
        for d in diffs:
            print(f'{d["name"]:40} {d["oldsize"]:10} {d["newsize"]:10}  {d["delta"]:+10}')
        print("RO Data")
        print(f"name                                            old        new       delta")
        diffs = val["readonly"]
        for d in diffs:
            print(f'{d["name"]:40} {d["oldsize"]:10} {d["newsize"]:10}  {d["delta"]:+10}')

    return values
