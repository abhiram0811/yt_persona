"""Quick test script to understand YouTube API responses."""

import os
from dotenv import load_dotenv
from ingestion.youtube_client import YouTubeClient

# Load environment variables
load_dotenv()

# Get API key from .env
api_key = os.getenv("YOUTUBE_API_KEY")
if not api_key:
    print("⚠️  YOUTUBE_API_KEY not found in .env file!")
    exit(1)

# Create client and test
client = YouTubeClient(api_key=api_key)
channel_id = "UCDHnXzXMy11cWm95J-Lw-bQ"  # Parker York Smith

print("=" * 60)
print("Testing: get_upload_playlist_id()")
print("=" * 60)

playlist_id = client.get_upload_playlist_id(channel_id)

print("\n" + "=" * 60)
print(f"🎉 Final Result: {playlist_id}")
print("=" * 60)
