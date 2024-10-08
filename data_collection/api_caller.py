import json
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
from dotenv import load_dotenv
import os


def get_api_key():
    load_dotenv()
    return os.environ['YOUTUBE_API_KEY']


def clean_transcript(dirty_transcript):
    cleaned_transcript = re.sub(r'\[.*?\]', '', dirty_transcript)
    cleaned_transcript = re.sub(r'\b[a-zA-Z]\b', '', cleaned_transcript)
    cleaned_transcript = re.sub(r'\s+', ' ', cleaned_transcript).strip()
    return cleaned_transcript


def get_video_data(video_id):
    try:
        youtube = build("youtube", "v3", developerKey=get_api_key())
        request = youtube.videos().list(part="snippet,statistics,contentDetails", id=video_id)
        response = request.execute()

        if response["items"]:
            video_info = response["items"][0]

            title = video_info["snippet"]["title"] if "title" in video_info["snippet"] else None
            description = video_info["snippet"]["description"] if "description" in video_info["snippet"] else None
            publishedAt = video_info["snippet"]["publishedAt"] if "publishedAt" in video_info["snippet"] else None
            tags = video_info["snippet"]["tags"] if "tags" in video_info["snippet"] else None
            category_id = video_info["snippet"]["categoryId"] if "categoryId" in video_info["snippet"] else None

            comment_count = video_info["statistics"]["commentCount"] if "commentCount" in video_info[
                "statistics"] else None
            duration = video_info["contentDetails"]["duration"] if "duration" in video_info["contentDetails"] else None

            video_data = {
                "video_id": video_id,
                "title": title,
                "description": description,
                "publishedAt": publishedAt,
                "tags": tags,
                "category_id": category_id,
                "comment_count": comment_count,
                "duration": duration
            }

            return video_data

        else:
            return None

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
            comment_count = video_info["statistics"]["commentCount"]

            return {
                "video_id": video_id,
                "views": views,
                "likes": likes,
                "comment_count": comment_count
            }
        else:
            return {"error": "Video niet gevonden of niet beschikbaar."}

    except Exception as e:
        print(f"Fout bij het ophalen van metadata: {e}")
        return None