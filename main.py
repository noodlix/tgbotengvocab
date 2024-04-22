import telebot
import requests

bot = telebot.TeleBot('7013468125:AAE5SgOciEi7vIfKuY1GneVIuQDZkKl4IF4')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Welcome, {message.from_user.first_name}! Send any word and I will provide you with a definition and an example.')

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'This bot helps you expand your English vocabulary.')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == 'new_word':
        send_new_word(message)
    else:
        word = message.text.lower()
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                definition = data[0]['meanings'][0]['definitions'][0]['definition']
                example = data[0]['meanings'][0]['definitions'][0].get('example', 'No example available')
                bot.send_message(message.chat.id, f'Definition of "{word}": {definition}\nExample: {example}')
            else:
                bot.send_message(message.chat.id, f'Word "{word}" not found.')
        except Exception as e:
            bot.send_message(message.chat.id, f'Error: {str(e)}')

bot.polling()
