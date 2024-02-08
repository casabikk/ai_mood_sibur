import telebot
from requests import get
from configuration.config import  bot_token
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import statistics
import os

bot = telebot.TeleBot(bot_token)
matplotlib.use('Agg')


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
        moods_dict = {}
        likes_dict = {}
        for com in data:
            mood_answer = get("http://127.0.0.1:8000/get_data", params = {'text': com['text']}).json()
            if mood_answer['mood'] is None:
                continue
            else:
                for mood in mood_answer['mood']:
                    if mood not in moods_dict:
                        moods_dict[mood] = 0
                    moods_dict[mood] += mood_answer["mood"][mood]

                for like in mood_answer['likes']:
                    if like not in likes_dict:
                        likes_dict[like] = 0
                    likes_dict[like] += mood_answer["likes"][like]          


        moods = list(moods_dict.values())
        likes = list(likes_dict.values())
        stat = list(filter(lambda a: a != 0, moods))
        if stat:
            average = statistics.mean(stat)
            median = statistics.median(stat)
            mode = statistics.mode(stat)
            value = sum(stat)
        else:
            average = 0 
            median = 0
            mode = 0

        plt.hist(moods, bins=10, color="red", edgecolor="black", label='Настроения')
        plt.plot(likes, label='Лайки')
        plt.legend()

        plt.xlabel('Номер настроения')
        plt.ylabel('Количество')                                                                                                                                 

        plt.savefig("hist1.png")
        plt.clf()
        with open("hist1.png", "rb") as media:
            bot.send_photo(message.chat.id, media, caption=f"Количвесто комментариев: " + str(value) +  '\nСреднее значение: ' + str(average) + '\n' + 'Медианное значение: ' + str(median) + '\n' + 'Мода: ' + str(mode) + "\n\nПример комметария:  " + str(data[0]['text']))
        os.remove("hist1.png")
bot.infinity_polling(none_stop=True)

