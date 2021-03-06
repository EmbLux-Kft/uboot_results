from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from ubtres.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static', static_url_path='/ubtestresults/static')
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)

    from ubtres.users.routes import users
    from ubtres.results.routes import results
    from ubtres.stats.routes import stats
    from ubtres.main.routes import main
    from ubtres.errors.handlers import errors
    from ubtres.api.routes import restapi
    app.register_blueprint(users, url_prefix='/ubtestresults')
    app.register_blueprint(results, url_prefix='/ubtestresults')
    app.register_blueprint(stats, url_prefix='/ubtestresults')
    app.register_blueprint(main, url_prefix='/ubtestresults')
    app.register_blueprint(errors, url_prefix='/ubtestresults')
    app.register_blueprint(restapi, url_prefix='/ubtestresults/api')

    return app
