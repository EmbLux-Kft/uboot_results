from flask import (make_response, flash, Blueprint, render_template)
from flask import current_app
from flask_login import current_user, login_required
from ubtres.utils import get_defconfig_data
from ubtres.utils import get_images_names
from ubtres.utils import convert_images_to_picture
from ubtres import db
from ubtres.models import Result
from ubtres.errors.handlers import error_404, error_416
# pip3 install matplotlib --user
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import json
import re

stats = Blueprint('stats', __name__)

def roundup(x):
    return x if x % 100 == 0 else x + 100 - x % 100

def rounddown(x):
    return x if x % 100 == 0 else x - 100 - x % 100

def side_values(num_list):
    mini = 10000000
    maxi = 0
    for n in num_list:
        if n < 0:
            continue
        if n > maxi:
            maxi = n
        if n < mini:
            mini = n
    return rounddown(mini), roundup(maxi)

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

def stats_diff_sizes(ids, dates, images):
    print("IDS ", ids)
    if (len(ids) < 2):
            return error_416("diff_sizes")
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
            return error_416("diff_sizes")

        val = {"commit":dates[i], "function":fd, "data":dd, "readonly":ro}
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


    # create the image
    fig = Figure(figsize=(14, len(values) * 7))
    row = 1
    for val in values:
        diffs = val["function"]
        axis = fig.add_subplot(len(values) * 2, 1, row)
        axis.set_title(f'diff size in bytes for commit {val["commit"]}')
        axis.set_xlabel("function")
        axis.set_ylabel("size in bytes")
        axis.grid(True)
        # get minimum and maximum
        xs = range(len(diffs))
        names = []
        deltap = []
        deltan = []
        for n in diffs:
            names.append(n["name"])
            if (n["delta"] >= 0):
                deltap.append(n["delta"])
            else:
                deltap.append(0)
            if (n["delta"] < 0):
                deltan.append(n["delta"])
            else:
                deltan.append(0)

        axis.set_xticks(xs)
        axis.set_xticklabels(names, rotation=90)
        axis.bar(names, deltap, width=1, color='r')
        axis.bar(names, deltan, width=1, color='b')
        row += 2

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@stats.route("/stats/<string:defconfig>/<string:imgtyp>/<int:count>")
def stats_defconfig(defconfig, imgtyp, count):
    count += 1
    ids, dates, images = get_defconfig_data(defconfig, count)
    if dates == None:
        return error_404(0)

    # shorten commit string to 6
    dates = [(d[:6] + '..') if len(d) > 6 else d for d in dates]

    if imgtyp == "diff_sizes":
        return stats_diff_sizes(ids, dates, images)

    images = convert_images_to_picture(images)
    img = None
    for n in images:
        if imgtyp == n["name"]:
            img = n
            break

    if img == None:
        return error_416(imgtyp)

    sz = img["values"]
    fig = Figure(figsize=(14, 9))
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title(f'{img["name"]} size in bytes')
    minv, maxv = side_values(sz)
    axis.set_xlabel("Commit ID")
    axis.grid(True)
    # get minimum and maximum
    axis.set_ylim([minv, maxv])
    xs = range(count)
    axis.set_xticks(xs)
    axis.set_xticklabels(dates, rotation=90)
    axis.plot(xs, sz, 'r*', label=img["name"])
    axis.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0., shadow=True)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@stats.route("/stats/<string:defconfig>/<int:count>")
def result_spl_uboot(defconfig, count):
    data = {"defconfig" : defconfig, "count" : str(count) }
    ids, dates, images = get_defconfig_data(defconfig, count)
    data["imagenames"] = get_images_names(images)
    return render_template('stats.html', title=f"Images for {defconfig}", data=data)
