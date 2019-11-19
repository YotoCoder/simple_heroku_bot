import os
from flask import Flask, request
import telebot

# Token que entrega el botfather de telegram
TOKEN = '123456:ABCDEFGHIJKLM'

# Url de la aplicación heroku
URL = 'https://nombre-de-la-aplicacion.herokuapp.com/'

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(func=lambda message: True, content_types=['new_chat_members'])
def echo_message(message):
	bot.send_message(message.chat.id, '<b>Bienvenide! '+message.new_chat_member.first_name + '</b>\n\n¿De donde eres?',parse_mode='HTML')

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

# Se debe ingresar la primera vez a la url para setear el Webhook del bot
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
