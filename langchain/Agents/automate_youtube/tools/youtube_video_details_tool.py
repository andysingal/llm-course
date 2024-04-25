# Look up all the information specific for Youtube

from typing import Type
from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
import os
import requests


class VideoDetails(BaseModel):
    title: str
    view_count: int
    like_count: int
    dislike_count: int
    comment_count: int
    channel_subscriber_count: int


class YoutubeVideoDetailsToolInput(BaseModel):
    """Input for YoutubeVideoDetailsTool."""
    video_id: str = Field(..., description="The ID of the YouTube video.")


class YoutubeVideoDetailsTool(BaseTool):
    name: str = "Get YouTube Video Details"
    description: str = "Retrieves details for a specific YouTube video."
    args_schema: Type[BaseModel] = YoutubeVideoDetailsToolInput

    def _run(self, video_id: str) -> VideoDetails:
        api_key = os.getenv("YOUTUBE_API_KEY")
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics",
            "id": video_id,
            "key": api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        item = response.json().get("items", [])[0]

        title = item["snippet"]["title"]
        view_count = int(item["statistics"]["viewCount"])
        like_count = int(item["statistics"].get("likeCount", 0))
        dislike_count = int(item["statistics"].get("dislikeCount", 0))
        comment_count = int(item["statistics"].get("commentCount", 0))

        channel_id = item["snippet"]["channelId"]
        channel_url = "https://www.googleapis.com/youtube/v3/channels"
        channel_params = {
            "part": "statistics",
            "id": channel_id,
            "key": api_key
        }
        channel_response = requests.get(channel_url, params=channel_params)
        channel_response.raise_for_status()
        channel_item = channel_response.json().get("items", [])[0]
        channel_subscriber_count = int(
            channel_item["statistics"]["subscriberCount"])

        return VideoDetails(
            title=title,
            view_count=view_count,
            like_count=like_count,
            dislike_count=dislike_count,
            comment_count=comment_count,
            channel_subscriber_count=channel_subscriber_count
        )
