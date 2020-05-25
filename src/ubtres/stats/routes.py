from flask import (make_response, flash, Blueprint, render_template)
from flask import current_app
from flask_login import current_user, login_required
from ubtres.utils import get_defconfig_data
from ubtres.utils import get_images_names
from ubtres.utils import convert_images_to_picture
from ubtres.utils import stats_get_diff_sizes
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

def create_stats_image(values):
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
        axis.bar(names, deltap, width=0.5, color='r')
        axis.bar(names, deltan, width=0.5, color='b')
        row += 2

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@stats.route("/stats/<string:defconfig>/<string:imgtyp>/<int:count>")
def stats_defconfig(defconfig, imgtyp, count):
    if imgtyp == "diff_sizes":
        values = stats_get_diff_sizes(defconfig, count)
        if values == None:
            return error_416("diff_sizes")
        return create_stats_image(values)

    ids, dates, images = get_defconfig_data(defconfig, count)
    if dates == None:
        return error_404(0)

    # shorten commit string to 8
    dates = [(d[:8] + '..') if len(d) > 8 else d for d in dates]


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
