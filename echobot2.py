import json 
import requests
import time
import random
import sys
import urllib.parse
from dbhelper import DBHelper

db = DBHelper()
TOKEN = "323240134:AAFx-CTiHigWevYKrbAw3hO89ftzc2yWb7g"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

leadIn = [
"Privet, Lena!",
"Hello Lena."
]

perpetrator = [
"Menya v armiu zabrali.",
"Ya shel po parku i na menya napal bomj."
]

delay = [
"Prosti menya pojaluista.",
"Ya bolshe tak ne budu."
]

data = [leadIn, perpetrator, delay]

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def makeExcuse(data):
  excuse = ""
  for column in data:
    rand = random.randint(0,(len(column)-1))
    excuse = excuse + column[rand] + " "
  return excuse

def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

#def main():
#    last_textchat = (None, None)
#    while True:
#        text, chat = get_last_chat_id_and_text(get_updates())
#        if (text, chat) != last_textchat:
#            text2 = makeExcuse(data)
#            send_message(text2, chat)
#            last_textchat = (text, chat)
#        time.sleep(0.5)


if __name__ == '__main__':
    main()