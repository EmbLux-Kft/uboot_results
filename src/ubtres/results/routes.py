from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,
                   send_from_directory, current_app)
from flask_login import current_user, login_required
from ubtres import db
from ubtres.models import Result
from ubtres.results.forms import ResultForm
import json

results = Blueprint('results', __name__)


@results.route("/result/new", methods=['GET', 'POST'])
@login_required
def new_result():
    form = ResultForm()
    if form.validate_on_submit():
        result = Result(title=form.title.data,
                build_date=form.build_date.data,
                arch=form.arch.data,
                cpu=form.cpu.data,
                soc=form.soc.data,
                toolchain=form.toolchain.data,
                basecommit=form.basecommit.data,
                boardname=form.boardname.data,
                defconfig=form.defconfig.data,
                images=form.images.data,
                content=form.content.data,
                author=current_user,
                success=form.success.data)
        db.session.add(result)
        db.session.commit()
        flash('Your new result is registered!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_result.html', title='New Result',
                           form=form, legend='New Result')


@results.route("/result/<int:result_id>")
def result(result_id):
    result = Result.query.get_or_404(result_id)

    result.json_images = json.loads(result.images)
    result.calc_values()
    return render_template('result.html', title=result.title, result=result)

@results.route("/result/files/results/<int:result_id>/<string:filename>")
def result_file(result_id, filename):
    return send_from_directory(current_app.config['STORE_FILES'] + f"/{result_id}",
                               filename, as_attachment=True)
