from flask import render_template, request, Blueprint
from ubtres.models import Result

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    results = Result.query.order_by(Result.date_posted.desc()).paginate(page=page, per_page=15)
    for r in results.items:
        r.basecommit_short = (r.basecommit[:8] + '..') if len(r.basecommit) > 6 else r.basecommit
    return render_template('home.html', results=results)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
@main.route("/announcements")
def announcements():
    return render_template('announcements.html', title='Announcements')
