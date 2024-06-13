from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from configuration.config import youtube_api_key


def get_youtube_client(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def get_youtube_video_name(url):
    api_key = youtube_api_key
    youtube = get_youtube_client(api_key)
    video_id = get_video_id_by_url(url)

    video_response = youtube.videos().list(
        id=video_id,
        part='snippet'
    ).execute()

    for video in video_response.get("items", []):
        name = video["snippet"]["title"]

    return name



def youtube_check_link(url):
    api_key = youtube_api_key
    youtube = get_youtube_client(api_key)
    video_id = get_video_id_by_url(url)
    try:
        request = youtube.videos().list(
            part="id",
            id=video_id
        )
        response = request.execute()
        
        if response.get("items"):
            return True
        else:
            return False
            
    except Exception as e:
        return False
    


def get_video_id_by_url(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None


def get_all_comments_youtube(video_url):
    api_key = youtube_api_key
    youtube = get_youtube_client(api_key)
    video_id = get_video_id_by_url(video_url)
    
    
    comments = []
    nextPageToken = None
    video_response = youtube.videos().list(
        id=video_id,
        part='snippet'
    ).execute()

    for video in video_response.get("items", []):
        name = video["snippet"]["title"]
        channel_id = video["snippet"]["channelId"]
    
    try:
        while True:
            response = youtube.commentThreads().list(
                part=['replies', 'snippet'],
                videoId=video_id,
                maxResults=100,  
                pageToken=nextPageToken,
                textFormat='plainText'
            ).execute()
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                likes = item['snippet']['topLevelComment']['snippet']['likeCount']
                date = item['snippet']['topLevelComment']['snippet']['publishedAt']
                comment_id = item['snippet']['topLevelComment']['id']
                user_id = item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
                comments.append({"platform" : 'Youtube', "channel_id": channel_id, "name": name, "user_id": user_id, "comment_id": comment_id, "text": comment, "likes": likes, "date": date.replace("T", " ").replace("Z", ""), "mood": -1})
                totalReplyCount = item['snippet']['totalReplyCount']
                if totalReplyCount > 0:
                    for reply in item['replies']['comments']:
                        user_id = reply['snippet']['authorChannelId']['value']
                        comment_id = reply['id']
                        likes = reply['snippet']['likeCount']
                        date = reply['snippet']['publishedAt']
                        comment_reply = reply['snippet']['textDisplay']
                        comments.append({"platform" : 'Youtube', "channel_id": channel_id, "name": name, "user_id": user_id, "comment_id": comment_id, "text": comment_reply, "likes": likes, "date": date.replace("T", " ").replace("Z", ""), "mood": -1})
                        
            nextPageToken = response.get('nextPageToken')
            if not nextPageToken:
                break
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    return comments
