from typing import Union
from fastapi import APIRouter
from models import Comments
from peewee import fn
import g4f

router = APIRouter()

@router.get("/get_comments")
def get_comments(user_text: str):
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


@router.get("/get_mood")
def get_mood(comments: str, message: str):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": f"{comments}\n\n\nДай мне оценку отношения этого текста к слову '{message}'. Оценка должна быть от 1 до 10, где 1 означает плохое отношение, а 10 - очень хорошее. ВАЖНО: ответить ты мне должен только одним числом от 1 до 10 и все, больше ничего отвечать не нужно"}],)
    
    return {"mood": response}