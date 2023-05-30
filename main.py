import praw
import telebot
import requests
import json
import cred

reddit = praw.Reddit(client_id=cred.CLIENTID,
                     client_secret=cred.SECRET,
                     user_agent=cred.USER)
bot = telebot.TeleBot(cred.TOKEN)

with open('fruits.txt', 'r') as u:
    f = json.load(u)

def collect(sub):
    for post in reddit.subreddit(sub).new():
        if post.url.endswith(('.jpg', '.jpeg', '.png')):
            if post.id not in f:
                response = requests.get(post.url)
                photo = response.content
                f.append(post.id)
                with open('fruits.txt', 'w') as t:
                    json.dump(f, t)
                return photo
            else:
                continue
    
@bot.message_handler(func=lambda message: True)
def send_photo(message):
    sub = message.text
    chatid = message.chat.id
    p = collect(sub)
    bot.send_photo(chat_id=chatid, photo=p, timeout=60)

bot.polling()