import time
import datetime
import requests
from configuration.config import vk_token
import re


def getjson(url, data=None):
    response = requests.get(url, params=data)
    response = response.json()
    return response

def get_owner_id(url):
    access_token = vk_token
    url2 = "https://api.vk.com/method/wall.get"
    params = {
        "domain": url.split("/")[-1],
        "access_token": access_token,
        "v": "5.131"
    }
    
    response = requests.get(url2, params=params)
    group_data = response.json()
    
    if "response" in group_data:
        owner_id = -group_data["response"]["items"][0]["owner_id"]
        return owner_id
    else:
        return None



def convert_to_iso8601(timestamp):
    dt_obj = datetime.datetime.utcfromtimestamp(timestamp)
    iso_time_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    return iso_time_str


def get_group_name(owner_id):
    access_token = vk_token
    url = "https://api.vk.com/method/groups.getById"
    params = {
        "group_id": owner_id,
        "access_token": access_token,
        "v": "5.131"
    }
    response = requests.get(url, params=params)
    group_data = response.json()
    group_name = group_data["response"][0]["name"]
    
    return group_name


def get_all_posts(access_token, owner_id, count=100, offset=0):
    print("Get all posts")
    all_posts = []
    while True:
        wall = getjson('https://api.vk.com/method/wall.get',
                       {'owner_id': owner_id, 'offset': offset, 'count': count, 'access_token': access_token, 'v': '5.131'})
        posts = wall['response']['items']

        all_posts.extend(posts)

        last_post_date = int(datetime.datetime.fromtimestamp(int(all_posts[-1]['date'])).strftime('%Y'))

        if last_post_date == 2015 or len(wall['response']['items']) == 0:
            break
        else:
            offset += 100
    return all_posts



def get_all_comments(access_token, owner_id, post_id, offset = 0):
    print("Get all comments")
    comments = []
    name = get_group_name(owner_id)
    for i in post_id:
        time.sleep(0.3)
        try:
            all_comments = getjson('https://api.vk.com/method/wall.getComments',
                           {'owner_id': -owner_id, 'post_id': i['id'], 'offset': offset, 'count': i['comments']['count'], 'access_token': access_token, 'need_likes': 1, 'v': '5.131'})
        except:
            break
        if all_comments.get('error'):
            print(all_comments['error'])
            continue
        if all_comments['response']['count'] == 0:
            continue
        for c in all_comments['response']['items']:
            if c['text'] != '':
                date = c['date']
                date = convert_to_iso8601(date)
                data = {'platform': 'Vk', 'channel_id': owner_id, 'name': name, 'user_id': c['from_id'], 'comment_id': c['id'], 'text': c['text'],  'likes': c['likes']['count'], 'date': date, 'mood': -1}
                print(data)
                comments.append(data)
    return comments



def get_all_comments_vk(owner_id):
    access_token = vk_token
    all_posts = get_all_posts(access_token, owner_id)

    post_id_list = []
    for i in all_posts:
        post_id_list.append(i['id'])

    comments = get_all_comments(access_token, owner_id, all_posts)

    return comments