## Origin
This is originally the project for 2022 Line Tech Fresh intern application, where we need to develop a line bot to promote ourselves, but I've also made a web version for it.

## How to Use It?
Click [here](https://dlccsimp.herokuapp.com/) to use the web version. 

Click [here](https://dlccsimp.herokuapp.com/line) to use the line bot version.

## Technical Aspects
The backend is powered by Flask, a lightweight Python web framework. The bot also stored some information about each user, using Heroku's free PostgreSQL. I use SQLAlchemy to integrate with it and Alembic to manage the models and do migrations.

The web frontend is very simple for now. But I might reskin it to become more chatbox like in the future.

## How to run it locally?
```
git clone https://github.com/dlccyes/dlcc_simp.git
```

```
pip3 install -r requirements.txt
```

Add `alembic.ini` in the project's root directory and correct `<your database URL>` to your database's URL
```
# alembic.ini
[alembic]

sqlalchemy.url = <your database URL>


[post_write_hooks]
# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

Add `.env` to the project's root directory, and add your own environmental variables.
```
TEST=true
LINE_BOT_CHANNEL_TOKEN=
LINE_BOT_CHANNEL_SECRET=
DATABASE_URL=
```