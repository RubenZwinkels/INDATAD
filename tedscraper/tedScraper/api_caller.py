import json
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re


def get_api_key():
    filename = "credentials.json"
    with open(filename, 'r') as file:
        config = json.load(file)
    return config.get('api_key')


def clean_transcript(dirty_transcript):
    cleaned_transcript = re.sub(r'\[.*?\]', '', dirty_transcript)
    cleaned_transcript = re.sub(r'\b[a-zA-Z]\b', '', cleaned_transcript)
    cleaned_transcript = re.sub(r'\s+', ' ', cleaned_transcript).strip()
    return cleaned_transcript


def get_video_data(video_id):
    try:
        youtube = build("youtube", "v3", developerKey=get_api_key())
        request = youtube.videos().list(part="snippet,statistics", id=video_id)
        response = request.execute()

        if response["items"]:
            video_info = response["items"][0]
            title = video_info["snippet"]["title"]
            description = video_info["snippet"]["description"]
            publishedAt = video_info["snippet"]["publishedAt"]

            return {
                "video_id": video_id,
                "title": title,
                "publishedAt": publishedAt
            }
        else:
            return {"error": "Video niet gevonden of niet beschikbaar."}

    except Exception as e:
        print(f"Fout bij het ophalen van metadata: {e}")
        return None


def get_video_captions(video_id):
    try:
        unformatted_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(unformatted_transcript)
        cleaned_transcript = clean_transcript(formatted_transcript)
        return cleaned_transcript
    except Exception as e:
        print(f"Fout bij het ophalen van ondertitels: {e}")
        return None

def get_video_info(video_id):
    metadata = get_video_data(video_id)
    transcript = get_video_captions(video_id)

    if "error" not in metadata:
        metadata['transcript'] = transcript
    return metadata

def get_video_statistic(video_id):
    try:
        youtube = build("youtube", "v3", developerKey=get_api_key())
        request = youtube.videos().list(part="snippet,statistics", id=video_id)
        response = request.execute()

        if response["items"]:
            video_info = response["items"][0]
            title = video_info["snippet"]["title"]
            description = video_info["snippet"]["description"]
            views = video_info["statistics"]["viewCount"]
            likes = video_info["statistics"].get("likeCount", None)

            return {
                "video_id": video_id,
                "views": views,
                "likes": likes
            }
        else:
            return {"error": "Video niet gevonden of niet beschikbaar."}

    except Exception as e:
        print(f"Fout bij het ophalen van metadata: {e}")
        return None