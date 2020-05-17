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
            if "B" in typ.upper():
                continue
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

def systemmap_get_size(d, c):
    for n in d:
        if n["name"] == c["name"] and n["typ"] == c["typ"]:
            return n["size"]

    return -1

def systemmap_calc_diffs(new, old):
    diffs = []
    for n in old:
        try:
            ns = systemmap_get_size(new, n)
            if ns == -1:
                continue
            if ns != n["size"]:
                delta = int(ns) - int(n["size"])
                diffs.append({"name":n["name"], "oldsize":n["size"], "newsize":ns, "delta":delta})
        except KeyError:
            pass
    return diffs

def stats_diff_sizes(ids, dates, images):
    values = []
    i = 0
    for uid in ids:
        print("UID ", uid)
        path = current_app.config['STORE_FILES'] + f"/{uid - 1}"
        fnold = f"{path}/System.map"
        path = current_app.config['STORE_FILES'] + f"/{uid}"
        fnnew = f"{path}/System.map"
        print("PATH ", fnold, fnnew)
        try:
            old = systemmap_to_dict(fnold)
            new = systemmap_to_dict(fnnew)
            systemmap_get_calc_sizes(old)
            systemmap_get_calc_sizes(new)
            diffs = systemmap_calc_diffs(new, old)
        except:
            print(f"not enough data file {fnold} {fnnew}")
            return error_416("diff_sizes")

        val = {"commit":dates[i], "sizediff":diffs}
        values.append(val)
        i += 1

    for val in values:
        print("Commit ", val["commit"])
        print(f"name                                            old        new       delta")
        diffs = val["sizediff"]
        for d in diffs:
            print(f'{d["name"]:40} {d["oldsize"]:10} {d["newsize"]:10}  {d["delta"]:+10}')

    # create the image
    fig = Figure(figsize=(14, len(values) * 7))
    row = 1
    for val in values:
        diffs = val["sizediff"]
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
