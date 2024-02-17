from typing import Union
from fastapi import APIRouter
from models import Comments, Mood
from peewee import fn
import g4f

router = APIRouter()

@router.get("/get_comments")
def get_comments(user_text: str):
    sql_query = f"""
        select *, text(text) <-> '{user_text}' as dist
        from public."Comments"
        where text(text) <-> '{user_text}' < 0.75
        order by dist"""
    comments = Comments.raw(sql_query)                             
    data = []
    for comment in comments:
        dict = {"comment_id": comment.comment_id, "person_id": comment.person_id, "date": comment.date, "text": comment.text, "parents_stack": comment.parents_stack, "post_id": comment.post_id, "likes": comment.likes}
        data.append(dict)
    if len(comments) == 0:
        return {"message": "Not found"}
    return {"message": "Found", "comments": data}



@router.get("/get_data")
def get_mood(text: str):
    query_mood = Mood.select().where(Mood.text == text)
    moods = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
    likes = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
    for mood in query_mood:
        if mood.mood not in moods or mood.mood not in likes:
            moods[mood.mood] = 0
            likes[mood.mood] = 0
        like = Comments.select().where(Comments.text == mood.comment)[0]
        likes[mood.mood] += like.likes
        moods[mood.mood] += 1
    
    if len(moods) == 0:
        return {"mood": None, 'likes': None}

    return {"mood": moods, "likes": likes}