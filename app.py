from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# get env from heroku config var
from dotenv import load_dotenv
import os
import re
import random

app = Flask(__name__)

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

def get_reply(msg):
    msg = msg.lower()
    msg_arr = re.split('[;,.\s\n]', msg)
    replymsg = list()

    if "hello" in msg_arr:
        replymsg.append((0, "Hey there sweatie 💕\nAsk me who am I pls."))

    if "who" in msg_arr:
        replymsg.append((0, "My name is Derrick, currently a junior in National Taiwan University, majoring in Electrical Engineering."))

    if "project" in msg_arr:
        default = True
        if "spotify" in msg_arr and "project" in msg_arr:
            replymsg.append((0, "You know what? You can just try it yourself!\nHere goes the link to the working site.\nhttps://playlastify.herokuapp.com/"))
            default = False
        if "glove" in msg_arr:
            replymsg.append((0, "Here's the github repo of the project, containing a detailed description and some demo videos!\nhttps://github.com/alwaysmle/Glove-Mouse"))
            default = False
        if default:
            replymsg.append((0, "I've done several projects, including:"))
            replymsg.append((0, "1. A full stack website analyzing and visualizing your playlists (say 'spotify project' to learn more)"))
            replymsg.append((0, "2. A glove that can replace your mouse and keyboard using Arduino, Python and ML (say 'glove project' to learn more)"))

    if "personal" in msg_arr and "website" in msg_arr:
        replymsg.append((0, "My personal website is\nhttps://dlccyes.github.io/"))

    if "resume" in msg_arr:
        replymsg.append((0, "Here goes my resume!\nhttps://dlccyes.github.io/resources/Derrick_Lin.pdf"))

    marsey_pic = ["marseydead", "marseyagreefast", "marseylove", "marseyhearts"]
    if "marsey" in msg_arr:
        # pic_id = random.randint(0, len(marsey_pic)-1)
        replymsg.append((1, f"https://rdrama.net/e/{random.choice(marsey_pic)}.webp"))


    if not replymsg: # no matches
        random_reply = ["idk what you're saying lol", "I know right?", "Everyone loves you ☺️"]
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
