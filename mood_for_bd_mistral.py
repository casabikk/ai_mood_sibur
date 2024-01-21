import llm
from peewee import *
from models import *
from models import Comments
from googletrans import Translator


def ai(message):
    model = llm.get_model("mistral-7b-openorca")
    bool = True
    try:
        response = model.prompt(message)
    except  Exception as e:
        print("Error")
        bool = False
    if not response.isdigit():
        print("нето")
        return None
    else:
        return response

def get_mood(comment):
    comment = f"{comment}\n\n\nТы - анатлитик, которому нужно проанализировать этот комментарий по отношению к компании Сибур. Определи настроение этого комментариия, где 0 - плохое, злое или печальное отношение к компании Сибур, а 10 - очень хорошее к компании Сибур.  ВАЖНО: ответить ты мне должен только одним числом от 1 до 10 и все, больше ничего отвечать не нужно"
    translator = Translator()
    data = translator.translate(comment, src='ru', dest='en')
    return ai(data)

def process_comments():
    moods = []
    for person in Comments.select():
        comment_id = person.comment_id
        comment = person.text
        mood = int(get_mood(comment))
        if mood is None:
            continue
        temp = {'comment_id': comment_id, 'comment': comment, 'mood': mood}
        moods.append(temp)
        print(temp)
    '''
    with connection:
        Mood.insert_many(moods).execute()'''

    print("Done")
    print(len(moods))
    
process_comments()
