from peewee import *
from util.models import *
from util.models import Comments
import string
import g4f


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
        


def get_mood(comment):
    data = [{"role": "user", "content": f"{comment}\n\n\n Выше написан комметарий. ВАЖНО: ответить ты мне должен только одним числом от 1 до 10 и все, больше ничего отвечать не нужно, даже если проанализировать этот комментарий ты не можешь. Ты - анатлитик, которому нужно проанализировать этот комментарий по отношению к компании Сибур, если комментарий отношения к Сибуру не имеет, то все равно оцени комметарий по 10бальной шкале, где 1 - отрицаительное мнение, а 10 максмимально одобряющее. Определи настроение этого комментариия, где 0 - плохое, злое или печальное отношение к компании Сибур, а 10 - очень хорошее к компании Сибур.   ВАЖНО: ответить ты мне должен только одним числом от 1 до 10 и все, больше ничего отвечать не нужно, даже если проанализировать этот комментарий ты не можешь"}]
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=data,
        )
        print(response)
    except Exception as e:
        print(e)
        print("Извините, произошла ошибка.")
        return None
    
    answer = check_for_digit(response)

    if answer is None:
        return None
    else:
        return answer


def check_in_moods(moods, comment_id):
    for mood in moods:
        if mood['comment_id'] == comment_id:
            return True
    return False 



def mood_me(moods):
    for person in moods:
        mood = None
        while mood is None:
            comment = person['text']
            mood = get_mood(comment)
            if mood is not None:
                person['mood'] = mood
            print(mood)    
    return moods