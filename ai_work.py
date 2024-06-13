from peewee import *
from models import *
import string
import requests
from configuration.config import LLM_TOKEN


def check_for_digit(text):
    text = text.split()
    text = [word.strip(string.punctuation) for word in text]
    for word in text:
        if word.isdigit():
            if int(word) >= 1 and int(word) <= 10:
                return word
    return None


def get_mood(comment):
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {"Authorization": "Bearer " + LLM_TOKEN}
    
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch response: {response.text}", "status_code": response.status_code}
    
    input_text = comment + " это комментарий, который оставил пользователь в группах связанных с компанией Сибур. Ты - аналитик, которому нужно проанализировать этот комментарий по отношению к компании Сибур. Если комментарий отношения к Сибур не имеет, то все равно оцени комментарий по 10-бальной шкале, где 1 - отрицательное мнение, а 10 максимально одобряющее. ВАЖНО: ответить ты мне должен только одним числом от 1 до 10 и все, больше ничего отвечать не нужно, даже если проанализировать этот комментарий ты не можешь."

    payload = {
        "inputs": input_text
    }

    output = query(payload)
    if 'error' not in output:
        if isinstance(output, list) and len(output) > 0:
            completion = output[0].get('generated_text', '')
            if completion.startswith(input_text):
                completion = completion[len(input_text):].strip()
            print(completion)
        else:
            print("Unexpected response format.")
    else:
        print(output['error'])

    answer = check_for_digit(completion)

    if answer is None:
        return None
    else:
        return answer


def mood_me(moods):
    new_moods = [] 
    for person in moods:
        attempts = 0 
        mood = None
        while mood is None and attempts < 5:  
            comment = person['text']
            mood = get_mood(comment)
            print(mood)
            attempts += 1  

        if mood is not None:
            person['mood'] = mood
            new_moods.append(person)  

    return new_moods
