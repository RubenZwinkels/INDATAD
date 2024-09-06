import requests
import json

def get_api_key():
    filename = "credentials.json"
    with open(filename, 'r') as file:
        config = json.load(file)
    return config.get('api_key')
def load_captions(video_id):
    # respone = requests.get("https://www.googleapis.com/youtube/v3", "key"="AIzaSyDYRQgz1fzxZDuLxemKU03BjiuZR68jub4")
    pass