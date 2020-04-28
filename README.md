## U-Boot Testresult server

## Installation

```bash
sudo dnf install python3-devel libffi-devel python-devel openssl-devel
```

clone this code and execute

```bash
pip3 install -r requirements.txt --user
```

## Start the server

```bash
source env_vars
python3 run.py
```

env_vars contains your secret setting. Example:

```
export SECRET_KEY="123456789abcdef0123456789abcdef1"
export SQLALCHEMY_DATABASE_URI="sqlite:///site.db"
export EMAIL_USER=<email to your email account>
export EMAIL_PASS=<password to your email account>
export FLASK_APP=run.py
export SERVER_PORT=5000
export SERVER_URL="http://127.0.0.1"
export SERVER_USER=<username>
export SERVER_PASSWORD=<password>
```

create secret key with:

```bash
python3 -c "import uuid; print(uuid.uuid4().hex)"
```

## Init the DB

```bash
flask db init
```

### mark user as admin

```bash
python3
Python 3.8.2 (default, Feb 28 2020, 00:00:00) 
[GCC 10.0.1 20200216 (Red Hat 10.0.1-0.8)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from ubtres.models import User, Result
>>> from ubtres import db, create_app
>>> app=create_app()
/home/hs/.local/lib/python3.8/site-packages/flask_sqlalchemy/__init__.py:793: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  warnings.warn(FSADeprecationWarning(
>>> ctx = app.app_context()
>>> ctx.push()
>>> 
>>> user = User.query.first()
>>> print(user)
User('hs', 'hs@denx.de', 'default.jpg', 'Simply me', 'None')
>>> user.isadmin=True
>>> print(user)
User('hs', 'hs@denx.de', 'default.jpg', 'Simply me', 'True')
>>> db.session.commit()
>
```

### update if model changes

```bash
flask db migrate -m "comment"
flask db upgrade
```

and you should have a new file in ```migrations/```
you should at to the commit.


## API

I put here an example file, which sends to the server
a new U-Boot testresult, see:

[client.py](src/client.py)


```bash
source env_vars
python3 client.py
```

## ToDo

- Discuss what infos we collect from an U-Boot build
- How to pass files to the server (tbot logfile, test.py result)
- How to make the server secure

## Notes

###SQLAlchemy Doku:

https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/

https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

### RGB colortable

http://www.markusbader.de/tricky/rgb_orange.html

### Bootstrap documentation

https://getbootstrap.com/docs/4.3/getting-started/introduction/
