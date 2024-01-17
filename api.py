from typing import Union
from fastapi import APIRouter
from models import Comments
from peewee import *

router = APIRouter()

@router.get("/get_comments/")
def get_comments(user_text: str):
    query = {'key': user_text}
    #comments = Comments.select().where(Comments.text ** f"%{user_text}%")
    #comments = Comments.select(Comments, fn.text(Comments.text).dist(user_text).alias('dist')).order_by(SQL('dist')).limit(30)
    sql_query = f"""
        select *, text(text) <-> '{user_text}' as dist
        from public."Comments" order by dist limit 10
    """

    comments = Comments.raw(sql_query)
                                    
    data = []
    for comment in comments:
        dict = {"comment_id": comment.comment_id, "person_id": comment.person_id, "date": comment.date, "text": comment.text, "parents_stack": comment.parents_stack, "post_id": comment.post_id, "likes": comment.likes}
        data.append(dict)

    if len(comments) == 0:
        return {"message": "Not found"}
    return {"message": "Found", "comments": data}