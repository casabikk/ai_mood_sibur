import telebot
from requests import get
from configuration.config import  bot_token

bot = telebot.TeleBot(bot_token)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, Я могу помочь тебе найти комментарий в группе Вконтакте паблика Сибур! Напиши любой текст, и я найду подходящий комментарий!")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    query = message.text  
    answer = get("http://127.0.0.1:8000/get_comments/", params = {'user_text': query}).json()
    if answer['message'] == "Not found":  
        bot.send_message(message.chat.id, "К сожалению таких комментариев нет(")
    else:
        data = answer['comments']
        if len(data) == 0:
            bot.send_message(message.chat.id, "К сожалению таких комментариев нет(")
        else:
            comments = ''
            for comment in data:
                comments += comment['text'] + '\n'
            answer2 = get("http://127.0.0.1:8000/get_mood", params = {'comments': comments, 'message': query}).json()
            aitxt = answer2['mood']
            if aitxt.isdigit():
                bot.send_message(message.chat.id, f"В группе Сибура к данному высказыванию относятся оценочно с настроением {aitxt}\10 ")
            else:
                bot.send_message(message.chat.id, f"Простите, не удалось определить отношение к тексту.")



bot.infinity_polling(none_stop=True)