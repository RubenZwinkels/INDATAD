import requests
import json
import googleapiclient
from googleapiclient.discovery import build

def get_api_key():
    filename = "credentials.json"
    with open(filename, 'r') as file:
        config = json.load(file)
    return config.get('api_key')

def get_video_captions(video_id):
    caption_id = get_captions_id(video_id)
    get_captions_by_id(caption_id)

def get_captions_by_id(caption_id):
    youtube = build("youtube", "v3", developerKey=get_api_key())
    request = youtube.captions().download(
        id=caption_id
    )
    response = request.execute()
    print(response)

def get_captions_id(video_id):
    youtube = build("youtube", "v3", developerKey=get_api_key())
    request = youtube.captions().list(
        part="snippet",
        videoId=video_id
    )
    response = request.execute()

    subtitles = response.get("items")
    correct_sub = None
    for subtitle in subtitles:
        if subtitle.get("snippet").get("language") == "en":
            correct_sub = subtitle

    if correct_sub == None:
        print(f"geen subtitles gevonden voor id: {video_id}")
        return None
    else:
        return correct_sub


def get_video_metadata(video_id):
    # Bouw de YouTube API service
    youtube = build("youtube", "v3", developerKey=get_api_key())

    # Maak een request om video-informatie op te halen
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id  # Video ID van de gewenste video
    )

    # Voer de request uit
    response = request.execute()

    # Controleer of er items zijn in de response
    if response["items"]:
        video_info = response["items"][0]
        # Haal de nodige metadata op
        title = video_info["snippet"]["title"]
        description = video_info["snippet"]["description"]
        views = video_info["statistics"]["viewCount"]
        likes = video_info["statistics"].get("likeCount", None)  # Gebruik None als geen likes beschikbaar zijn

        # Bouw en retourneer een nette dict met de metadata
        return {
            "video_id": video_id,
            "title": title,
            "description": description,
            "views": int(views),
            "likes": int(likes) if likes is not None else None  # Controleer of likes niet None is voordat je het omzet naar een int
        }
    else:
        # Retourneer een lege dict of een melding als de video niet gevonden is
        return {"error": "Video niet gevonden of niet beschikbaar."}