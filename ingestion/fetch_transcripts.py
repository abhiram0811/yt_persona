import json
import time
from pathlib import Path
import os
from dotenv import load_dotenv
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)
from ingestion.youtube_client import YouTubeClient

load_dotenv()

# Get credentials from .env
api_key = os.getenv("YOUTUBE_API_KEY")
channel_id = os.getenv("CHANNEL_ID")

ytt_api = YouTubeTranscriptApi()
client = YouTubeClient(api_key=api_key)


def fetch_transcript_channel(channel_id: str):
    videos = client.get_channel_videos(channel_id)

    for vid in videos:
        vid_id = vid["video_id"]
        file_path = Path(f"../data/raw/transcripts/{vid_id}.json")
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure dir exists
        if file_path.exists():
            print(f"⏩ Skipping {vid_id} (already exists)")
            continue
        try:
            transcript = ytt_api.fetch(vid_id)
            snippets = transcript.snippets
            data = [
                {"text": s.text, "start": s.start, "duration": s.duration}
                for s in snippets
            ]
            final_data = vid.copy()
            final_data["transcript"] = data

            with open(file_path, "w") as f:
                json.dump(final_data, f, indent=2)

            print(f"✅Saved transcript: {vid_id} ({len(data)}lines)")
        except (TranscriptsDisabled, NoTranscriptFound):
            print(f"⚠️ No transcript for {vid_id}, skipping.")
        except Exception as e:
            print(f" Error Fetching {vid_id}: {e}")
        time.sleep(0)


if __name__ == "__main__":
    print(f"🚀 Starting transcript fetch for channel: {channel_id}")
    fetch_transcript_channel(channel_id)
