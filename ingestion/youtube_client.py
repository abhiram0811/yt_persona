from googleapiclient.discovery import build


class YouTubeClient:
    """Client for interating with the Youtube Data API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        pass

    def get_channel_videos(self, channel_id: str):
        youtube = build("youtube", "v3", developerKey=self.api_key)
        playlist_id = self.get_upload_playlist_id(channel_id)
        next_page_token = None
        videos = []
        while True:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token,
            )
            response = request.execute()
            for item in response["items"]:
                snippet = item["snippet"]
                video_id = snippet["resourceId"]["videoId"]
                title = snippet["title"]
                description = snippet["description"]
                tags = snippet.get("tags", [])
                published_at = snippet["publishedAt"]
                url = f"https://www.youtube.com/watch?v={video_id}"

                video_data = {
                    "video_id": video_id,
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "published_at": published_at,
                    "url": url,
                }
                videos.append(video_data)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return videos

    def get_upload_playlist_id(self, channel_id: str) -> str:
        """Get the uploads playlist ID for a channel."""
        youtube = build("youtube", "v3", developerKey=self.api_key)
        request = youtube.channels().list(part="contentDetails", id=channel_id)
        response = request.execute()
        uploads_id = response["items"][0]["contentDetails"]["relatedPlaylists"][
            "uploads"
        ]
        print(f"\n✅ Extracted uploads playlist ID: {uploads_id}")
        return uploads_id
