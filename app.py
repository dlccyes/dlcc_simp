from flask import Flask, request, abort

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

app = Flask(__name__)

# database
from sqlalchemy import create_engine, select, MetaData, Table, insert, delete, update

if not os.getenv('DATABASE_URL'):
    # get variable from local .emv
    # from config import *
    from dotenv import load_dotenv
    load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
engine = create_engine(DATABASE_URL)
conn = engine.connect()

metadata = MetaData(bind=None)
chat_t = Table(
    'chat_t', 
    metadata, 
    autoload=True, 
    autoload_with=engine
)

# Channel Access Token
channel_access_token = os.getenv('LINE_BOT_CHANNEL_TOKEN')
line_bot_api = LineBotApi(channel_access_token)
# Channel Secret
channel_secret = os.getenv('LINE_BOT_CHANNEL_SECRET')
handler = WebhookHandler(channel_secret)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback(): # webhook
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # text = request.json['events'][0]['message']['text']
    print(f'🥺🥺🥺{request.json}')
    app.logger.info("Request body: " + body)
    app.logger.info("💕💕💕")
    # handle webhook body
    try:
        handler.handle(body, signature)
        # get message count from database
        msg_count = db_get('msg_count')
        # update message count to database
        db_update('msg_count', msg_count+1)

    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = TextSendMessage(text=event.message.text)
    
    replymsg = get_reply(event.message.text)
    print(replymsg)
    message = list()
    # max 5 replies
    for msg in replymsg:
        if msg[0] == 0: # text
            message.append(TextSendMessage(text=msg[1]))
        elif msg[0] == 1: # image
            message.append(ImageSendMessage(original_content_url=msg[1], preview_image_url=msg[1]))
    line_bot_api.reply_message(event.reply_token, message)

def db_get(clmn):
    """get value of clmn from database"""
    stmt = select(chat_t.c[clmn]).where(chat_t.c.identity=='main')
    results = conn.execute(stmt).fetchall()
    return results[0][0]

def db_update(clmn, val):
    """update value of clmn to database"""
    stmt = chat_t.update().where(chat_t.c.identity=='main').values({clmn:val})
    conn.execute(stmt)

def have_word(words, word_set, _and=False):
    "if a word in words is in word_set, return True"
    # all match
    if _and:
        for word in words:
            if word not in word_set:
                return False
        return True
    # one match
    for word in words:
        if word in word_set:
            print(f'{word} is a match')
            return True
    return False

def get_reply(msg):
    msg = msg.lower()
    word_list = re.split('[;,.!?\s\n]', msg)
    word_set = set(word_list)
    print(word_set)
    replymsg = list()

    if msg == 'help':
        replymsg.append((0, "Hi! I'm Derrick Lin.\nYou can ask me about my experiences, projects, or skills (in English)."))
        replymsg.append((0, "You can tell me your name, and I'll remember it.\nYou can also reply 'message count' to get the number of messages I've received from you."))
        return replymsg

    if msg == 'message count':
        msg_count = db_get('msg_count')
        replymsg.append((0, f"You've sent me {msg_count} messages since I started counting it ☺️"))
        return replymsg

    if "my name is" in msg:
        name = msg.replace("my name is", "")
        name = name.strip(' ')
        if not name:
            replymsg.append((0, "Uhh what 🤔🤔🤔\nWhat's your name again?"))
            return replymsg
        name = name[0].upper() + name[1:]
        replymsg.append((0, f"Hi {name}, I'm Derrick. Nice to meet you!"))
        replymsg.append((1, "https://rdrama.net/e/marseyblush.webp"))
        db_update('username', name)
        return replymsg

    if have_word(['hi', 'hello', 'hey', 'yo'], word_set):
        name = db_get('username')
        if name:
            replymsg.append((0, f"Hi {name}, I'm Derrick. Ask me anything!"))
        else:
            replymsg.append((0, "Hello stranger! What's your name?"))

    if have_word(['who'], word_set):
        replymsg.append((0, "My name is Derrick, currently a junior in National Taiwan University, majoring in Electrical Engineering."))

    if have_word(['intern', 'internship', 'interns', 'internships', 'experience', 'experiences', 'work'], word_set):
        replymsg.append((0, "I've interned in Rushpay, a startup focusing on providing a unified interface for ordering and various payment systems for merchants.\nHere's their website: https://rushbit.net"))
        replymsg.append((0, "I worked as a backend developer there, and I've completed many full stack features in PHP/Laravel and JavaScript that were later on deployed to production, used by tens of thousands of customers."))
        replymsg.append((0, "I've also helped them automate their CI/CD pipeline with Gitlab Runner and Google Kubernetes Engine, making the deployment process become faster and more convenient."))
        return replymsg

    if have_word(['project', 'projects'], word_set):
        default = True
        if have_word(['spotify'], word_set):
            replymsg.append((0, "I've made a full stack Spotify stat website, and you know what? You can try it yourself!\nHere goes the link to the working site.\nhttps://playlastify.herokuapp.com/"))
            replymsg.append((0, "Here's a screenshot of the website."))
            replymsg.append((1, "https://i.imgur.com/fKjx5lW.png"))
            replymsg.append((0, "Beautiful, isn't it?"))
            default = False
        if have_word(['glove'], word_set):
            replymsg.append((0, "Here's the github repo of my glove project, containing a detailed description and some demo videos!\nhttps://github.com/alwaysmle/Glove-Mouse"))
            default = False
        if default:
            replymsg.append((0, "I've done several projects, including:"))
            replymsg.append((0, "1. A full stack website analyzing and visualizing your playlists (say 'spotify project' to learn more)"))
            replymsg.append((0, "2. A glove that can replace your mouse and keyboard using Arduino, Python and ML (say 'glove project' to learn more)"))
        return replymsg

    if have_word(['personal', 'website'], word_set) or have_word(['contact'], word_set):
        replymsg.append((0, "My personal website is\nhttps://dlccyes.github.io/.\nYou can find lots of information about me here!"))
    
    if have_word(['github'], word_set):
        replymsg.append((0, "My github account is\nhttps://github.com/dlccyes.\nYou can also go to my personal website to learn more about me!\nhttps://dlccyes.github.io/"))

    if have_word(['resume', 'cv'], word_set):
        replymsg.append((0, "Here goes my resume!\nhttps://dlccyes.github.io/resources/Derrick_Lin.pdf"))

    if have_word(['skill', 'skills', 'skillset'], word_set):
        replymsg.append((0, "Through my internship experience, the projects I've made and the courses I've taken, I've acquired many skills, including:"))
        replymsg.append((0, "Languages: Python, C/C++, JavaScript/HTML/CSS, PHP, SQL, RISC-V Assembly, Verilog, R, MATLAB\n\n\
Frameworks and Libraries: jQuery, Laravel, Django, PyTorch\n\n\
Tools: Git, Linux, MySQL, MongoDB, Docker, K8s, GCP, Heroku"))

    marsey_pic = ["marseyagreefast", "marseyblowkiss", "marseyhearts", "marseyblush", "marseymarseylove"]
    if "marsey" in word_set:
        replymsg.append((1, f"https://rdrama.net/e/{random.choice(marsey_pic)}.webp"))

    if not replymsg: # no matches
        random_reply = ["I know right?", "Everyone loves you ☺️"]
        if(random.randint(0, 1)):
            replymsg.append((0, random.choice(random_reply)))
        else:
            replymsg.append((1, f"https://rdrama.net/e/{random.choice(marsey_pic)}.webp"))

    # max 5 replies
    if len(replymsg) > 5:
        replymsg = ["Sorry, please ask something else 🥲"]

    return replymsg

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
