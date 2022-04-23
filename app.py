from platform import platform
from flask import Flask, request, abort, render_template, url_for, redirect

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import os

import re
import random
from datetime import datetime
import json

app = Flask(__name__)

# database
from sqlalchemy import create_engine, select, MetaData, Table, insert, delete, update

if not os.getenv('DATABASE_URL'):
    # get variable from local .emv
    # from config import *
    from dotenv import load_dotenv
    load_dotenv()


testing = False
if os.getenv('TEST') == 'true': 
    testing = True

# Channel Access Token
channel_access_token = os.getenv('LINE_BOT_CHANNEL_TOKEN')
line_bot_api = LineBotApi(channel_access_token)
# Channel Secret
channel_secret = os.getenv('LINE_BOT_CHANNEL_SECRET')
handler = WebhookHandler(channel_secret)

@app.route("/")
def index_page():
    return render_template('index.html')

@app.route("/line")
def add_line_page():
    return render_template('line.html')

@app.route("/getWebResponse", methods=['POST'])
def web_response():
    try:
        print(f'{request}')
        rqst = request.get_json()
        print(f'💕💕{rqst}')
        handle_reqest = RequestController(rqst)
        replymsg = handle_reqest.get_reply(msg=handle_reqest.msg)
        return {'success':1, 'replies': replymsg}
    except Exception as e:
        print(e)
        return {'success':0}

@app.route("/callback", methods=['POST'])
def line_response(): # line webhook
    print(f'{request}')
    print(f'🥺🥺🥺{request.json}')
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # text = request.json['events'][0]['message']['text']
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)
    return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
@handler.add(MessageEvent)
def handle_message(event):
    message = list()
    try: 
        rqst = json.loads(str(event))
        print(rqst)
        handle_reqest = RequestController(rqst)

        replymsg = handle_reqest.get_reply(msg=handle_reqest.msg)

        print(replymsg)
        # max 5 replies
        #TODO
        # TemplateSendMessage
        for msg in replymsg:
            if msg[0] == 0: # text
                message.append(TextSendMessage(text=msg[1]))
            elif msg[0] == 1: # image
                message.append(ImageSendMessage(original_content_url=msg[1], preview_image_url=msg[1]))
    except Exception as e:
        print(e)
        message.append(TextSendMessage(text="I'm sleeping right now 😴😴\nPlease try again later."))

    line_bot_api.reply_message(event.reply_token, message)

class RequestController():
    def __init__(self, request):
        DATABASE_URL = os.getenv('DATABASE_URL')
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
        engine = create_engine(DATABASE_URL)
        self.conn = engine.connect()

        metadata = MetaData(bind=None)
        self.chat_t = Table(
            'chat_t', 
            metadata, 
            autoload=True, 
            autoload_with=engine
        )
        if 'source' in request and 'userId' in request['source']:
            self.identity = request['source']['userId']
        else:
            self.identity = 'web'
        if not self.db_get('id'): # no entry for this identity
            # TODO
            if 'replyToken' in request: # line
                platform = 0
            else: # web
                platform = 1
            stmt = self.chat_t.insert().values(identity=self.identity, platform=platform)
            self.conn.execute(stmt)
        self.platform = self.db_get('platform')

        self.word_set = set()
        self.msg = None
        if 'message' in request and 'text' in request['message']:
            self.msg = request['message']['text']

        # check time passed since last message
        time_now = datetime.now()
        last_msg_time_str = self.db_get('last_msg_time')
        if last_msg_time_str:
            last_msg_time = datetime.fromisoformat(last_msg_time_str)
            time_passed = time_now - last_msg_time
            # 1 hr since last message -> reset memory
            if testing:
                memory_time_out = 30
            else:
                memory_time_out = 3600
            if time_passed.seconds > memory_time_out:
                self.db_update('username', None)
                self.db_update('msg_count', 0)
        # update date & time of last message to database
        self.db_update('last_msg_time', time_now.isoformat())

        # get message count from database
        msg_count = self.db_get('msg_count')
        if not msg_count:
            msg_count = 0
        # update message count to database
        self.db_update('msg_count', msg_count+1)

    def db_get(self, clmn):
        """get value of clmn from database"""
        stmt = select(self.chat_t.c[clmn]).where(self.chat_t.c.identity==self.identity)
        results = self.conn.execute(stmt).fetchall()
        if not results or not results[0]: return False
        return results[0][0]

    def db_update(self, clmn, val):
        """update value of clmn to database"""
        stmt = self.chat_t.update().where(self.chat_t.c.identity==self.identity).values({clmn:val})
        self.conn.execute(stmt)

    def have_word(self, words, _and=False):
        "if a word in words is in word_set, return True"
        # all match
        if _and:
            for word in words:
                if word not in self.word_set:
                    return False
            return True
        # one match
        for word in words:
            if word in self.word_set:
                return True
        return False

    def get_marsey(self):
        marsey_pic = ["marseyagreefast", "marseyblowkiss", "marseyhearts", "marseyblush", "marseymarseylove"]
        return f"https://rdrama.net/e/{random.choice(marsey_pic)}.webp"

    def get_reply(self, msg=None):
        replymsg = list()
        if not msg: msg = self.msg 
        try:
            #msg = event.message.text
            print(msg)
            msg = msg.lower()
            word_list = re.split('[;,.!?\s\n]', msg)
            self.word_set = set(word_list)
        except Exception as e:
            print(e)
            replymsg.append((1, self.get_marsey()))
            return replymsg

        if msg == 'help':
            replymsg.append((0, "Hi! I'm Derrick Lin.\nYou can ask me about my experiences, projects, or skills (in English)."))
            replymsg.append((0, "You can tell me your name, and I'll remember it.\nYou can also reply 'message count' to get the number of messages I've received from you."))
            replymsg.append((0, "btw I have a short memory, so I'll forget everything 1 hour after your last message."))
            return replymsg

        if msg == 'message count':
            msg_count = self.db_get('msg_count')
            replymsg.append((0, f"You've sent me {msg_count} messages as far as I can recall ☺️"))
            return replymsg

        if "my name is" in msg:
            name = msg[msg.find("my name is")+len("my name is"):]
            name = name.strip(' ')
            if not name:
                replymsg.append((0, "Uhh what 🤔🤔🤔\nWhat's your name again?"))
                return replymsg
            name = name[0].upper() + name[1:]
            replymsg.append((0, f"Hi {name}, I'm Derrick. Nice to meet you!"))
            replymsg.append((1, "https://rdrama.net/e/marseyblush.webp"))
            self.db_update('username', name)
            return replymsg

        if self.have_word(['hi', 'hello', 'hey', 'yo']):
            name = self.db_get('username')
            if name:
                replymsg.append((0, f"Hi {name}, I'm Derrick. Ask me anything!"))
            else:
                replymsg.append((0, "Hello stranger! What's your name?"))

        if self.have_word(['who']):
            replymsg.append((0, "My name is Derrick, currently a junior in National Taiwan University, majoring in Electrical Engineering."))

        if self.have_word(['intern', 'internship', 'interns', 'internships', 'experience', 'experiences', 'work']):
            replymsg.append((0, "I've interned in Rushpay, a startup focusing on providing a unified interface for ordering and various payment systems for merchants.\nHere's their website: https://rushbit.net"))
            replymsg.append((0, "I worked as a backend developer there, and I've completed many full stack features in PHP/Laravel and JavaScript that were later on deployed to production, used by tens of thousands of customers."))
            replymsg.append((0, "I've also helped them automate their CI/CD pipeline with Gitlab Runner and Google Kubernetes Engine, making the deployment process become faster and more convenient."))
            return replymsg

        if self.have_word(['project', 'projects']):
            default = True
            if self.have_word(['spotify']):
                replymsg.append((0, "I've made a full stack Spotify stat website, and you know what? You can try it yourself!\nHere goes the link to the working site.\nhttps://playlastify.herokuapp.com/"))
                replymsg.append((0, "Here's a screenshot of the website."))
                replymsg.append((1, "https://i.imgur.com/fKjx5lW.png"))
                replymsg.append((0, "Beautiful, isn't it?"))
                default = False
            if self.have_word(['glove']):
                replymsg.append((0, "Here's the github repo of my glove project, containing a detailed description and some demo videos!\nhttps://github.com/alwaysmle/Glove-Mouse"))
                default = False
            if default:
                replymsg.append((0, "I've done several projects, including:"))
                replymsg.append((0, "1. A full stack website analyzing and visualizing your playlists (reply 'spotify project' to learn more)"))
                replymsg.append((0, "2. A glove that can replace your mouse and keyboard using Arduino, Python and ML (reply 'glove project' to learn more)"))
            return replymsg

        if self.have_word(['personal', 'website']) or self.have_word(['contact']):
            replymsg.append((0, "My personal website is\nhttps://dlccyes.github.io/.\nYou can find lots of information about me here!"))
        
        if self.have_word(['github']):
            replymsg.append((0, "My github account is\nhttps://github.com/dlccyes.\nYou can also go to my personal website to learn more about me!\nhttps://dlccyes.github.io/"))

        if self.have_word(['resume', 'cv']):
            replymsg.append((0, "Here goes my resume!\nhttps://dlccyes.github.io/resources/Derrick_Lin.pdf"))

        if self.have_word(['skill', 'skills', 'skillset']):
            replymsg.append((0, "Through my internship experience, the projects I've made and the courses I've taken, I've acquired many skills, including:"))
            replymsg.append((0, "Languages: Python, C/C++, JavaScript/HTML/CSS, PHP, SQL, RISC-V Assembly, Verilog, R, MATLAB\n\nFrameworks and Libraries: jQuery, Laravel, Django, PyTorch\n\nTools: Git, Linux, MySQL, MongoDB, Docker, K8s, GCP, Heroku"))

        if self.have_word(['marsey']):
            replymsg.append((1, self.get_marsey()))

        if not replymsg: # no matches
            random_reply = ["I know right?", "Everyone loves you ☺️"]
            if(random.randint(0, 1)):
                replymsg.append((0, random.choice(random_reply)))
            else:
                replymsg.append((1, self.get_marsey()))

        # max 5 replies
        if len(replymsg) > 5:
            replymsg = ["Sorry, please ask something else 🥲"]

        return replymsg

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
