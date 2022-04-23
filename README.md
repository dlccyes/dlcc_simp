# dlcc simp
A bot that knows everything (the professional aspects) about me, and it's happy to tell you all of it, as long as you ask the correct questions.

## Demo
### line version
![](/resources/line_demo.webp)

### web version
![](/resources/web_demo.webp)

## How to use It?
Click [here](https://dlccsimp.herokuapp.com/) to use the web version. 

Click [here](https://dlccsimp.herokuapp.com/line) to use the line bot version.

Enter `help` to know what to ask!
## Origin
This is originally the project for 2022 Line Tech Fresh intern application, where we need to develop a line bot to promote ourselves, but I've also made a web version for it.

## Technical Aspects
The backend is powered by Flask, a lightweight Python web framework. To make the bot seems more humane, it will "remember" some information about each user, using Heroku's free PostgreSQL database. I use SQLAlchemy to integrate with the database and Alembic to manage the models and do migrations.

The web frontend is very simple for now. But I might reskin it to become more chatbox like in the future.

## How to run it?
### Download the codes
```
git clone https://github.com/dlccyes/dlcc_simp.git
```

### Install required packages
```
pip3 install -r requirements.txt
```

### Add environment files
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
For the line bot credentials and other things, refer to [this guide](https://developers.line.biz/en/docs/messaging-api/building-sample-bot-with-heroku/#deploy-the-echo-sample-bot).

Note that if you just want to use the web version, you won't need the line credentials. They're for the line bot version.

### Do database migrations
After setting up your database and pointing to your databse in env files, you'll need to do migrations to create necessary tables and columns for this project.

At the project root, run
```
alembic upgrade head
```

You can learn more about SQLAlchemy & Alembic [here](https://dlccyes.github.io/CollegeNotes/OtherNotes/Programming/SQLAlchemy.html).

### Deploy the bot
Now the bot is ready! 

If you want to use the line bot version, deploy it to heroku, add the callback endpoint in your line bot setting, add your bot as friend and start chatting! 

To use the web version, just run
```
python3 app.py
```
and go to your localhost to interact with the bot!

You can also deploy it to heroku (or other services) to make it available everywhere!
