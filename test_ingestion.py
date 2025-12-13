"""
Quick test script to verify YouTube ingestion works.
"""

import os
from dotenv import load_dotenv
from ingestion.youtube_client import YouTubeClient

load_dotenv()

# Get credentials from .env
api_key = os.getenv("YOUTUBE_API_KEY")
channel_id = os.getenv("CHANNEL_ID")

print("🎬 Testing YouTube Client...")
print(f"Channel ID: {channel_id}\n")

# Create client and fetch videos
client = YouTubeClient(api_key=api_key)
videos = client.get_channel_videos(channel_id)

# Display results
print(f"\n{'=' * 50}")
print(f"✅ SUCCESS! Fetched {len(videos)} total videos")
print(f"{'=' * 50}\n")

# Show first 3 videos
print("📹 Sample videos:")
for i, video in enumerate(videos[:3], 1):
    print(f"\n{i}. {video['title']}")
    print(f"   ID: {video['video_id']}")
    print(f"   Published: {video['published_at']}")
    print(f"   URL: {video['url']}")
    print(f"   Tags: {video['tags'][:3] if video['tags'] else 'None'}...")
