## U-Boot Testresult server

This is just a proof of concept for discussion.

Find an example running server here:

http://xeidos.ddns.net/ubtestresults/home

Running for the wandboard DL a tbot [testcase](https://github.com/EmbLux-Kft/tbot-tbot2go/blob/wandboard-devel-messe/tc/wandboard/tc_wandboard.py#L208)
from a cron job once a day and push with tbot [generator](https://github.com/EmbLux-Kft/tbot/blob/devel/generators/push-testresult.py)
the results to this server. Here an example log:

```bash
$ tbot @argswandboardlab1 wandboard_ub_build_install_test -q -q
tbot starting ...
├─Flags:
│ 'lab-1-build'
├─Calling wandboard_ub_build_install_test ...
│   ├─Calling wandboard_ub_build ...
│   │   ├─Calling uboot_build ...
│   │   │   ├─Calling uboot_checkout ...
│   │   │   │   ├─Builder: wandboard-builder
│   │   │   │   └─Done. (1.410s)
│   │   │   ├─Add toolchain to PATH /work/hs/tbot-workdir/toolchain/gcc-linaro-7.3.1-2018.05-x86_64_arm-linux-gnueabi/bin
│   │   │   ├─Cleaning previous build ...
│   │   │   ├─Configuring build ...
│   │   │   ├─Patching U-Boot config ...
│   │   │   ├─Calling kconfig_set_value ...
│   │   │   │   ├─Setting CONFIG_LOCALVERSION to "-tbot" ...
│   │   │   │   └─Done. (0.006s)
│   │   │   ├─Calling uboot_make ...
│   │   │   │   └─Done. (34.843s)
│   │   │   └─Done. (40.402s)
│   │   ├─Calling copy ...
│   │   │   └─Done. (0.003s)
│   │   ├─Calling copy ...
│   │   │   └─Done. (0.003s)
│   │   ├─Calling copy ...
│   │   │   └─Done. (0.003s)
│   │   ├─Calling copy ...
│   │   │   └─Done. (0.003s)
│   │   ├─Calling copy ...
│   │   │   └─Done. (0.003s)
│   │   └─Done. (40.801s)
│   ├─Calling wandboard_ub_install ...
│   │   ├─POWERON (wandboard)
│   │   ├─UBOOT (wandboard-uboot)
│   │   ├─POWEROFF (wandboard)
│   │   └─Done. (12.368s)
│   ├─Calling wandboard_ub_check_version ...
│   │   ├─found in image U-Boot version U-Boot 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 14:58:35 +0200)
│   │   ├─found in image U-Boot SPL version U-Boot SPL 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 14:58:35 +0200)
│   │   ├─POWERON (wandboard)
│   │   ├─UBOOT (wandboard-uboot)
│   │   ├─found U-Boot SPL version U-Boot SPL 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 14:58:35 +0200) installed
│   │   ├─found U-Boot version U-Boot 2020.04-tbot-00687-gd16d37bcd4 (Apr 28 2020 - 14:58:35 +0200) installed
│   │   ├─POWEROFF (wandboard)
│   │   └─Done. (8.925s)
│   ├─Calling uboot_testpy ...
│   │   ├─Calling uboot_setup_testhooks ...
│   │   │   ├─Creating FIFOs ...
│   │   │   ├─Hooks are up to date, skipping deployment ...
│   │   │   ├─Adding hooks to $PATH ...
│   │   │   ├─Open console & command channels ...
│   │   │   └─Done. (0.024s)
│   │   ├─Calling uboot_checkout ...
│   │   │   ├─Builder: wandboard-builder
│   │   │   └─Done. (1.430s)
│   │   ├─POWERON (wandboard)
│   │   ├─UBOOT (wandboard-uboot)
│   │   ├─POWEROFF (wandboard)
│   │   └─Done. (24.600s)
│   └─Done. (86.696s)
├─────────────────────────────────────────
├─Log written to '/home/hs/data/Entwicklung/wandboard/tbot-tbot2go/log/lab1-wandboard-0168.json'
└─SUCCESS (86.852s)
$ ./push-testresult.py -p /home/hs/data/Entwicklung/tbot/
log/lab1-wandboard-0168.json -> results/pushresults/lab1-wandboard-0168.txt
```

Which leads to the result on the server:

[U-Boot test result](http://xeidos.ddns.net/ubtestresults/result/45)


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
