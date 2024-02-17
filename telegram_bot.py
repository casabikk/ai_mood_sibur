import telebot
import yaml
from requests import get
from configuration.config import  bot_token
from DB_add import db_add_comments
from mood_g4f import *
from youtube import *
from vk import *
import matplotlib.pyplot as plt
import matplotlib
import statistics
import os
                                                        
bot = telebot.TeleBot(bot_token)
matplotlib.use('Agg')
  

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, Я могу помочь тебе найти комментарий в группе Вконтакте паблика Сибур! Напиши любой текст, и я найду подходящий комментарий!")


@bot.message_handler(commands=['check'])
def check_channels(message):
    data= yaml.safe_load(open("configuration/yaml.yml", encoding='utf-8'))
    vk = []
    for elem in data["vk"]:
        for name, v_url in elem.items():
            vk.append(f'<a href="{v_url}">{name}</a>')

    youtube = []
    for elem in data["youtube"]:
        for name, y_url in elem.items():
            youtube.append(f'<a href="{y_url}">{name}</a>')
    bot.send_message(message.chat.id, f"<b>Vk</b>:\n{'\n- '.join(vk)}\n\n<b>Youtube</b>:\n{'\n- '.join(youtube)}\n\n<i>Чтобы добавить в аналитику новое сообщество или видео напишите /add и cсылку на видео или group-id сообщества.</i>", parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(commands=['add'])
def check_channels(message):
    text = message.text
    text = ''.join(text.split()[1:]).strip()
    if text.startswith("https://www.youtube.com/watch") or text.startswith("https://youtu.be/"):
        check = youtube_check_link(text)
        if not check:
            bot.send_message(message.chat.id, "Некорректная ссылка на видео")
        else:
            video = get_youtube_video_name(text)
            with open('configuration/yaml.yml', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            if video in data["youtube"]:
                bot.send_message(message.chat.id, "Такое видео уже добавлено")
            else:
                comments = get_all_comments_youtube(text)
                comments = mood_me(comments)
                db_add_comments(comments)
                new_youtube_url = {video: text}
                data["youtube"].append(new_youtube_url)
                bot.send_message(message.chat.id, "Комментарии добавлены в аналитику")
            with open('configuration/yaml.yml', 'w', encoding='utf-8') as file:
                yaml.dump(data, file, allow_unicode=True)

    elif text.startswith("https://vk.com/"):
        owner_id = get_owner_id(text)
        print(owner_id)
        if owner_id is None:
            bot.send_message(message.chat.id, "Некорректная ссылка на группу")
        else:
            name = get_group_name(owner_id)
            with open('configuration/yaml.yml', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            if name in data["vk"]:
                bot.send_message(message.chat.id, "Такое сообщество уже добавлено")
            else:
                comments = get_all_comments_vk(owner_id)
                comments = mood_me(comments)
                db_add_comments(comments)
                new_vk_url = {name: text}
                data["vk"].append(new_vk_url)
                bot.send_message(message.chat.id, "Комментарии добавлены в аналитику")
            with open('configuration/yaml.yml', 'w', encoding='utf-8') as file:
                yaml.dump(data, file, allow_unicode=True)
    else:
        bot.send_message(message.chat.id, "Некорректная ссылка на группу или видео")


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

