import base64
from datetime import datetime, timedelta
import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from ubtres import db, login_manager, bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    isadmin = db.Column(db.Boolean(), default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    about = db.Column(db.String(120), nullable=False, default="--")
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    results = db.relationship('Result', backref='author', lazy=True)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def check_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    #'last_seen': self.last_seen.isoformat() + 'Z',
    #'post_count': self.posts.count(),

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.about}', '{self.isadmin}')"

# from
# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def human_size(num: int) -> str:
    base = 1
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']:
        n = num / base
        if n < 9.95 and unit != 'B':
            # Less than 10 then keep 1 decimal place
            value = "{:.1f}{}".format(n, unit)
            return value
        if round(n) < 1000:
            # Less than 4 digits so use this
            value = "{}{}".format(round(n), unit)
            return value
        base *= 1024
    value = "{}{}".format(round(n), unit)
    return value

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    build_date = db.Column(db.DateTime, nullable=False)
    arch = db.Column(db.String(20), nullable=False)
    cpu = db.Column(db.String(20), nullable=True)
    soc = db.Column(db.String(20), nullable=False)
    toolchain = db.Column(db.String(100), nullable=False)
    basecommit = db.Column(db.String(40), nullable=False)
    boardname = db.Column(db.String(100), nullable=True, default="unknown")
    defconfig = db.Column(db.String(40), nullable=False)
    splsize = db.Column(db.Integer, nullable=True)
    ubsize = db.Column(db.Integer, nullable=True)
    success = db.Column(db.Boolean(), default=True)
    content = db.Column(db.Text, nullable=False)

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        data = {
            'title' : self.title,
            'build_date': self.build_date,
            'arch': self.arch,
            'cpu': self.cpu,
            'soc': self.soc,
            'toolchain': self.toolchain,
            'basecommit': self.basecommit,
            'boardname' : self.boardname,
            'defconfig': self.defconfig,
            'splsize': self.splsize,
            'ubsize': self.ubsize,
            'content': self.content,
            'success': self.success,
        }
        return data

    def from_dict(self, data):
        for field in ['title', 'arch', 'cpu', 'soc', 'toolchain', 'basecommit', 'boardname', 'defconfig', 'splsize', 'ubsize', 'content']:
            if field in data:
                setattr(self, field, data[field])
        # handle build_date
        self.build_date = datetime.strptime(data["build_date"], "%Y-%m-%d %H:%M:%S")
        # handle "success"
        if isinstance(data["success"], str):
            for s in ["True", "true", "1"]:
                if s == data["success"]:
                    data["success"] = True
                    break
        if isinstance(data["success"], str):
            data["success"] = False
        self.success = data["success"]

    def calc_values(self):
        self.splsizekib = human_size(self.splsize)
        self.ubsizekib = human_size(self.ubsize)

    def __repr__(self):
        return f"Result('{self.title}', '{self.build_date}', '{self.arch}', '{self.soc}', '{self.toolchain}', '{self.basecommit}', '{self.boardname}', '{self.defconfig}', '{self.splsize}', '{self.ubsize}', '{self.date_posted}', '{self.success}')"
