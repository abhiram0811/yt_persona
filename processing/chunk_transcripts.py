from vectorstore.pinecone_client import upsert_chunk
import json
from pathlib import Path


def chunk_transcripts(
    transcripts_dir: str = "data/raw/transcripts", chunk_duration: int = 30
):
    transcripts_path = list(Path(transcripts_dir).glob("*.json"))
    print("📂 Files found:", transcripts_path)
    for file_path in transcripts_path:
        with open(file_path) as f:
            data = json.load(f)
            print(f"📹 Processing: {data['video_id']} - {data['title'][:50]}...")

            chunks = {}

            for snippet in data["transcript"]:
                start_time = snippet["start"]
                text = snippet["text"]
                chunk_number = int(start_time / chunk_duration)
                if chunk_number not in chunks:
                    chunks[chunk_number] = []
                chunks[chunk_number].append(text)

            for chunk_num, texts in chunks.items():
                combined_text = " ".join(texts)
                chunk_start = chunk_num * chunk_duration
                chunk_id = f"{data['video_id']}_chunk_{chunk_num}"

                upsert_chunk(
                    chunk_id=chunk_id,
                    text=combined_text,
                    metadata={
                        "video_id": data["video_id"],
                        "title": data["title"],
                        "start_time": chunk_start,
                        "text": combined_text[:1000],
                    },
                )
                print(
                    f"  ✅ Chunk {chunk_num} ({chunk_start}s) - {len(combined_text)} chars"
                )

            print(f"✅ Completed {data['video_id']}: {len(chunks)} chunks\n")


def main():
    chunk_transcripts()


if __name__ == "__main__":
    main()
