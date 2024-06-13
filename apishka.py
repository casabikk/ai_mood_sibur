from fastapi import APIRouter
from models import Comments
from datetime import datetime

router = APIRouter()

from fastapi import APIRouter

router = APIRouter()
@router.get("/get_comments")
async def get_comments(user_text: str):
    prepared_text = ' & '.join(user_text.split()) + ':*'

    sql_query = """
        SELECT *,
        ts_rank_cd(to_tsvector('russian', text), plainto_tsquery('russian', %s)) AS rank
        FROM public."Comments"
        WHERE to_tsvector('russian', text) @@ plainto_tsquery('russian', %s)
        ORDER BY rank DESC
        LIMIT 100;  -- Ограничиваем результат 100 записями для избежания перегрузки
    """
    
    comments = Comments.raw(sql_query, prepared_text, prepared_text)
    
    data = []
    for comment in comments:
        try:
            date_obj = datetime.strptime(comment.date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            date_obj = comment.date 
        print(comment.date)
        data.append({
            "channel_id": comment.channel_id,
            "comment_id": comment.comment_id,
            "date": date_obj.strftime('%Y-%m-%d %H:%M:%S') if isinstance(date_obj, datetime) else comment.date,
            "text": comment.text,
            "user_id": comment.user_id,
            "mood": comment.mood,
            "likes": comment.likes,
            "platform": comment.platform
        })

    if not data:
        return {"message": "Not found"}
    
    return {"message": "Comments found", "comments": data}



@router.get("/get_data")
def get_mood(text: str):
    query_mood = Comments.get(Comments.text == text)
    return {"mood": query_mood.mood, "likes": query_mood.likes}