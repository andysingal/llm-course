# Something specific video topics we want to learn
# And find 10 ~ 15 videos on that subject

from typing import List, Type
from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field 

import os
import requests
from datetime import datetime, timezone 

class VideoSearchResult(BaseModel):
    video_id: str
    title: str
    channel_id: str
    channel_title: str
    days_since_published: int 

class YoutubeVideoSearchToolInput(BaseModel):
    keyword: str = Field(..., description="The keyword to search for.")
    max_results: int = Field(10, description="The maximum number of results to return.")

class YoutubeVideoSearchTool(BaseTool):
    name: str = "Search YouTube Videos"
    description: str = "Search for videos on a specific topic and return the first 10-15 results."
    args_schema: Type[BaseModel] = YoutubeVideoSearchToolInput

    def _run(self, keyword: str, max_results: int = 10) -> List[VideoSearchResult]:
        api_key = os.getenv("YOUTUBE_API_KEY", None)
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": keyword,
            "type": "video",
            "maxResults": max_results,
            "key": api_key,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])

        results = []
        for item in items:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            channel_id = item["snippet"]["channelId"]
            channel_title = item["snippet"]["channelTitle"]
            publish_date = datetime.fromisoformat(item["snippet"]["publishedAt"].replace('Z', '+00:00')).astimezone(timezone.utc)
            days_since_published = (datetime.now(timezone.utc) - publish_date).days
            results.append(VideoSearchResult(video_id, title, channel_id, channel_title, days_since_published))
        return results