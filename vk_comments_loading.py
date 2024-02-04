import time
import datetime
import requests
from configuration.config import vk_token, owner_id, oowner_id
from DB_add import db_add_comments, db_add_person

access_token = vk_token

def getjson(url, data=None):
    response = requests.get(url, params=data)
    response = response.json()
    return response


def get_all_posts(access_token, owner_id, count=100, offset=0):
    all_posts = []
    while True:
        time.sleep(0.3)
        wall = getjson('https://api.vk.com/method/wall.get',
                       {'owner_id': owner_id, 'offset': offset, 'count': count, 'access_token': access_token, 'v': '5.131'})
        posts = wall['response']['items']

        all_posts.extend(posts)

        last_post_date = int(datetime.datetime.fromtimestamp(int(all_posts[-1]['date'])).strftime('%Y'))

        if last_post_date == 2015 or wall['response']['items'] == []:
            break
        else:
            offset += 100
    return all_posts
def get_all_liked_lists(access_token, owner_id, liked_object_id, count=1000, offset=0, friends_only=0):
    List_of_users = []
    for i in liked_object_id:
        time.sleep(0.3)
        api_query = getjson('https://api.vk.com/method/likes.getList',
                            {'access_token': access_token, 'type': 'post', 'owner_id': owner_id, 'item_id': i,
                             'filter': 'likes', 'friends_only': friends_only, 'count': count, 'v': '5.131'})
        List_of_users.append(api_query['response']['items'])

    return List_of_users
def get_all_ids(access_token, owner_id):
    offset = 0
    count = 1000
    all_ids_loc = []
    time.sleep(0.2)
    first = getjson('https://api.vk.com/method/groups.getMembers',
                      {'group_id': owner_id, 'offset': offset, 'count': count, 'access_token': access_token,
                       'fields': 'id',
                       'v': '5.131'})
    for i in range(first['response']['count'] // 1000):
        time.sleep(0.2)
        members = getjson('https://api.vk.com/method/groups.getMembers',
                          {'group_id': owner_id, 'offset': offset, 'count': count, 'access_token': access_token, 'fields': 'id',
                           'v': '5.131'})
        offset += 1000
        for j in range(count-1):
            try:
                all_ids_loc.append(members['response']['items'][j]['id'])
            except:
                break
    if first['response']['count'] % 1000 != 0:
        time.sleep(0.2)
        members = getjson('https://api.vk.com/method/groups.getMembers',
                          {'group_id': owner_id, 'offset': offset, 'count': first['response']['count'] % 1000, 'access_token': access_token,
                           'fields': 'city',
                           'v': '5.131'})
        for j in range(count - 1):
            try:
                all_ids_loc.append(members['response']['items'][j]['id'])
            except:
                break
    return all_ids_loc
def get_all_comments(access_token, owner_id, post_id, offset = 0):
    comments = []
    for i in post_id:
        try:
            time.sleep(0.3)
            all_comments = getjson('https://api.vk.com/method/wall.getComments',
                            {'owner_id': owner_id, 'post_id': i['id'], 'offset': offset, 'count': i['comments']['count'], 'access_token': access_token, 'need_likes': 1, 'v': '5.131'})
        except:
            break
        if all_comments['response']['count'] == 0:
            continue
        for c in all_comments['response']['items']:
            if c['text'] != '':
                comments.append({'comment_id': c['id'], 'person_id': c['from_id'], 'date': c['date'], 'text': c['text'], 'parents_stack': c['parents_stack'], 'post_id': i['id'], 'likes': c['likes']['count']})
    return comments
def user_and_likes(all_ids, list_of_liked):
    user_likes = {}
    for j in all_ids:
        user_likes[j] = 0
    for i in list_of_liked:
        for l in i:
            for k in all_ids:
                if(l == k):
                    user_likes[k] += 1
    return user_likes
def user_and_comments(comments, all_ids):
    user_comments = {}
    for k in all_ids:
        user_comments[k] = 0
    for i in comments:
        for j in all_ids:
            if(i['person_id'] == j):
                user_comments[j] += 1
    return user_comments
all_posts = get_all_posts(access_token, owner_id)

post_id_list = []
for i in all_posts:
    post_id_list.append(i['id'])

list_of_liked = get_all_liked_lists(access_token, owner_id, post_id_list)

all_ids = get_all_ids(access_token, oowner_id)

user_likes = user_and_likes(all_ids, list_of_liked)

comments = get_all_comments(access_token, owner_id, all_posts)

user_comments = user_and_comments(comments, all_ids)

person = []
for i in range(len(all_ids)):
    person.append({'person_id': all_ids[i], 'likes_count': user_likes[all_ids[i]], 'comments_count': user_comments[all_ids[i]]})

db_add_person(person)
db_add_comments(comments)

print("Done")