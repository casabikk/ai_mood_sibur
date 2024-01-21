from peewee import *
from models import *
from models import Comments
import string
import g4f
import asyncio

def trim(text, max_length=4096):
    current_length = sum(len(message["content"]) for message in text)
    while text and current_length > max_length:
        removed_message = text.pop(0)
        current_length -= len(removed_message["content"])
    return text


def check_for_digit(text):
    text = text.split()
    text = [word.strip(string.punctuation) for word in text]
    for word in text:
        if word.isdigit():
            if int(word) >= 1 and int(word) <= 10:
                return word
    return None
        


async def get_mood(comment):
    '''ua = fake_useragent.UserAgent()
    headers = {'User-Agent': ua.random}
    all_proxy = open('proxy.txt').read().split('\n')
    ip = choice(all_proxy).strip()'''
    ip = '45.153.20.222:11812'
    proxy =  f'http://{ip}'

    data = [{"role": "user", "content": f"{comment}\n\n\n Выше написан комметарий. ВАЖНО: ответить ты мне должен только одним числом от 1 до 10 и все, больше ничего отвечать не нужно, даже если проанализировать этот комментарий ты не можешь. Ты - анатлитик, которому нужно проанализировать этот комментарий по отношению к компании Сибур, если комментарий отношения к Сибуру не имеет, то все равно оцени комметарий по 10бальной шкале, где 1 - отрицаительное мнение, а 10 максмимально одобряющее. Определи настроение этого комментариия, где 0 - плохое, злое или печальное отношение к компании Сибур, а 10 - очень хорошее к компании Сибур.   ВАЖНО: ответить ты мне должен только одним числом от 1 до 10 и все, больше ничего отвечать не нужно, даже если проанализировать этот комментарий ты не можешь"}]
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            messages=data,
            providers=g4f.Provider.Bard,
        )
        print(response)
        print(1)
    except Exception as e:
        print("Извините, произошла ошибка.")
        return None
    
    answer = check_for_digit(response)

    if answer is None:
        return None
    else:
        return answer






async def process_comments():
    moods = []
    print(len(Comments.select()))
    for person in Comments.select():
        comment_id = person.comment_id
        print(comment_id)
        comment = person.text
        mood = await asyncio.create_task(get_mood(comment))
        if mood is None:
            continue

        temp = {'comment_id': comment_id, 'comment': comment, 'mood': int(mood)}
        moods.append(temp)
        print(temp)
    
    with connection:
        Mood.insert_many(moods).execute()

    print("Done")
    print(len(moods))
    
asyncio.run(process_comments())
