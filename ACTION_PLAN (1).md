# ACTION_PLAN.md — ParkerStyle Advisor (Web Scraping + RAG Pipeline)

## Project Goal
Build a **portfolio-grade, production-style ingestion + RAG pipeline** using publicly available YouTube data from *Parker York Smith* to create a **fashion & lifestyle AI assistant** that:

- Extracts video metadata + transcripts ethically via official APIs  
- Cleans, chunks, and enriches the data  
- Embeds chunks and stores them in **Pinecone** with metadata  
- Serves answers in a Parker-inspired style (not impersonation)  
- Cites video URLs and sources  
- Provides a clean, modular architecture suitable for real-world scraping needs (mirrors Visalaw-style ingestion tasks)

This project is **personal + educational**, focused on skill-building in:
- ingestion pipelines  
- rate-limited scraping  
- processing/cleaning  
- VDB usage  
- metadata modeling  
- RAG system design  
- automation patterns  

---

# 1. System Architecture Overview

```
YouTube API (Metadata + Transcripts)
           |
           v
   ingestion/ (fetch_videos, fetch_transcripts)
           |
           v
 processing/ (cleaning, chunking, metadata enrichment)
           |
           v
 vectorstore/ (embeddings -> Pinecone)
           |
           v
      API/ (FastAPI RAG pipeline)
           |
           v
 UI/nextjs or Streamlit (Chat UI)
```

Additional components:

- **scripts/** → automation tasks (sync new videos, run full ingestion)
- **configs/** → API keys, settings
- **tests/** → unit tests for ingestion + chunking + RAG logic

---

# 2. Directory Structure (Create this layout)

```
parkerstyle/
  ingestion/
    youtube_client.py
    fetch_videos.py
    fetch_transcripts.py
  processing/
    cleaning.py
    chunking.py
    enrich_metadata.py
    types.py
  vectorstore/
    pinecone_client.py
    upsert.py
  api/
    main.py
    rag_pipeline.py
  ui/
    next-app/  (or streamlit_app.py)
  configs/
    settings.yaml
  scripts/
    run_full_ingestion.py
    sync_new_videos.py
  tests/
    test_chunking.py
    test_ingestion.py
  ACTION_PLAN.md
```

---

# 3. Ingestion Layer — Tasks

## 3.1 Implement YouTube Client
- Use `google-api-python-client`
- Required features:
  - Retrieve channel upload playlist
  - Paginate through all videos (50 per page)
  - Extract:
    - video_id  
    - title  
    - description  
    - tags  
    - published date  
    - video URL  

## 3.2 Save Raw Metadata
Save each video as a raw JSON blob:

```
data/raw/videos/{video_id}.json
```

## 3.3 Fetch Transcripts
Use `youtube_transcript_api` and save to:

```
data/raw/transcripts/{video_id}.txt
```

## 3.4 Add Rate Limiting + Retries
- Sleep randomly between calls  
- Exponential backoff on errors  

## 3.5 Add Incremental Sync
Track last ingestion timestamp in:

```
data/state/last_ingested.json
```

Only ingest new videos.

---

# 4. Processing Layer — Tasks

## 4.1 Cleaning
- Remove repeated captions  
- Strip emojis (optional)  
- Normalize whitespace  

## 4.2 Chunking
- Chunk into ~800-character segments  
- Create internal `Chunk` model:

```python
Chunk {
  id,
  video_id,
  title,
  url,
  published_at,
  start_sec,
  end_sec,
  text,
  topics: [],
  style_tags: [],
  outfit_links: []
}
```

## 4.3 Extract Outfit Links
- Parse video descriptions  
- Extract URL links  
- Attach them at video level or into relevant chunks

## 4.4 Topic Classification (optional)
Use LLM to generate tags:
- wardrobe basics  
- fit & proportions  
- lifestyle & mindset  
- shopping  

## 4.5 Save Processed Chunks
Write to:

```
data/processed/chunks/{video_id}.json
```

---

# 5. Vector Store Layer — Tasks

## 5.1 Setup Pinecone Index
- Dimensions: `1536`  
- Metric: cosine  
- Metadata fields:  
  - title  
  - video_id  
  - url  
  - topics  
  - style_tags  
  - published_at  

## 5.2 Embed Text Chunks
Use OpenAI embeddings (`text-embedding-3-small`).

## 5.3 Upsert Pipeline
Bulk insert vectors with metadata using Pinecone’s Python client.

## 5.4 Validate Index
Check record count and metadata integrity.

---

# 6. API Layer (FastAPI)

## 6.1 Endpoints
```
POST /ask
GET  /health
GET  /debug/chunk/{id}
```

## 6.2 Retrieval Logic
- Embed user query  
- Query Pinecone  
- Return top_k matches  

## 6.3 Parker-Inspired Style Prompt
Warm, encouraging tone; practical advice; cite sources.  
Explicitly describe assistant as “AI assistant inspired by Parker York Smith”, not Parker himself.

## 6.4 Response Schema

```json
{
  "answer": "...",
  "tips": ["...", "..."],
  "sources": [
    {
      "title": "...",
      "url": "...",
      "score": 0.87
    }
  ]
}
```

---

# 7. UI Layer (Next.js or Streamlit)

## 7.1 Features
- Chat interface  
- Displays AI reply  
- Shows citations (video titles + URLs)  

## 7.2 Enhancements (Optional)
- Session memory  
- Style-selector (minimal, streetwear, formal)  
- “Open video” buttons  

---

# 8. Automation & DevOps Notes

## 8.1 Create `sync_new_videos.py`
Runs ingestion → processing → upsert and updates `last_ingested.json`.

## 8.2 Scheduling
Choose:
- Cron  
- GitHub Actions scheduled workflow  
- Python `schedule` loop  

## 8.3 Logging
Log ingestion events, chunk counts, Pinecone upserts, and errors using `logging` or `structlog`.

## 8.4 Environment Variables

Create `.env`:

```
YOUTUBE_API_KEY=
OPENAI_API_KEY=
PINECONE_API_KEY=
CHANNEL_ID=
```

Load with `python-dotenv`.

---

# 9. Testing Plan

## 9.1 Ingestion Tests
- Test pagination  
- Test metadata parsing  
- Test handling of missing fields  

## 9.2 Processing Tests
- Test chunk sizes and boundaries  
- Test cleaning removes noise  
- Test link extraction from descriptions  

## 9.3 RAG Tests
- Test retrieval behavior with a known query phrase  
- Ensure sources include correct URLs and titles  

---

# 10. Milestone Timeline

## Day 1
- Create repo + folder structure  
- Implement YouTube client  
- Fetch + save all metadata  

## Day 2
- Fetch transcripts  
- Add rate limiting + error handling  
- Save raw transcripts  

## Day 3
- Implement cleaning + chunking  
- Extract outfit links  
- Save processed chunks  

## Day 4
- Setup Pinecone index  
- Implement embedding + upsert flow  
- Validate index contents  

## Day 5
- Build RAG pipeline in FastAPI  
- Implement Parker-inspired style prompt  
- Add source citations in responses  

## Day 6
- Build UI (Next.js or Streamlit)  
- Hook UI to FastAPI backend  

## Day 7
- Implement automation (`sync_new_videos.py`)  
- Add logging  
- Cleanup, polish, write README, record demo GIF/screenshot  

---

# 11. Deliverables

## Required
- Full ingestion → processing → vector DB → API → UI pipeline  
- Clean architecture and modular code  
- Working chat UI  
- README + screenshots / GIF demo  

## Optional (Portfolio Boost)
- Topic classification per chunk via LLM  
- Shopping suggestions mapping to non-affiliate product pages  
- Dockerization of API + ingestion  
- API docs (Swagger / OpenAPI)  

---

# 12. How This Maps to Visalaw Work

Trains skills in:

- ETL pipelines  
- API-driven ingestion  
- Metadata modeling  
- Vector search and RAG orchestration  
- Automation engineering (scheduled syncs)  

These apply directly to:

- Immigration policy synchronization  
- Agency website/document change detection  
- Dataset updating & indexing  
- Internal legal QA tooling  

---
