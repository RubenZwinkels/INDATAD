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
    youtube = build("youtube", "v3", developerKey= get_api_key())
    request = youtube.captions().list(
        part = "snippet",
        videoId = video_id
    )
    response = request.execute()
    print(json.dumps(response, sort_keys=True, indent=4))


def get_video_metadata(video_id):
    # Bouw de YouTube API service
    youtube = build("youtube", "v3", developerKey= get_api_key())

    # Maak een request om video-informatie op te halen
    request = youtube.videos().list(
        part="snippet,statistics",
        # Onderdeel van de video: snippet voor titel/beschrijving en statistics voor likes/views
        id=video_id  # Video ID van de gewenste video
    )

    # Voer de request uit
    response = request.execute()

    # Haal de metadata op als de video gevonden is
    if response["items"]:
        video_info = response["items"][0]
        title = video_info["snippet"]["title"]
        description = video_info["snippet"]["description"]
        views = video_info["statistics"]["viewCount"]
        likes = video_info["statistics"].get("likeCount", "Geen likes beschikbaar")

        # Print de informatie
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Views: {views}")
        print(f"Likes: {likes}")
    else:
        print("Video niet gevonden of niet beschikbaar.")