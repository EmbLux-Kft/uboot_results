from flask import (make_response, flash, Blueprint, render_template)
from flask_login import current_user, login_required
from ubtres.utils import get_defconfig_data
from ubtres import db
from ubtres.models import Result
from ubtres.errors.handlers import error_404, error_416
# pip3 install matplotlib --user
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

stats = Blueprint('stats', __name__)

def roundup(x):
    return x if x % 100 == 0 else x + 100 - x % 100

def rounddown(x):
    return x if x % 100 == 0 else x - 100 - x % 100

def side_values(num_list):
    results_list = sorted(num_list)
    return rounddown(results_list[0]), roundup(results_list[-1])

@stats.route("/stats/<string:defconfig>/<string:imgtyp>/<int:count>")
def stats_defconfig(defconfig, imgtyp, count):
    dates, splsizes, ubsizes = get_defconfig_data(defconfig, count)
    if dates == None:
        return error_404(0)

    # shorten commit string to 6
    dates = [(d[:6] + '..') if len(d) > 6 else d for d in dates]
    us = ubsizes
    ss = splsizes
    fig = Figure(figsize=(14, 9))
    axis = fig.add_subplot(1, 1, 1)
    if imgtyp == 'u-boot':
        axis.set_title("U-Boot size in bytes")
        minv, maxv = side_values(ubsizes)
    else:
        axis.set_title("SPL size in bytes")
        minv, maxv = side_values(splsizes)
    axis.set_xlabel("Commit ID")
    axis.grid(True)
    # get minimum and maximum
    axis.set_ylim([minv, maxv])
    xs = range(count)
    axis.set_xticks(xs)
    axis.set_xticklabels(dates, rotation=90)
    try:
        if imgtyp == 'u-boot':
            axis.plot(xs, us, label=f"U-Boot")
        else:
            axis.plot(xs, ss, label=f"SPL")
    except:
        return error_416(count)

    #axis.plot(xs, ss, label=f"SPL")
    axis.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0., shadow=True)

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@stats.route("/stats/<string:defconfig>/<int:count>")
def result_spl_uboot(defconfig, count):
    data = {"defconfig" : defconfig, "count" : count }
    return render_template('stats.html', title=f"SPL / U-Boot for {defconfig}", data=data)
