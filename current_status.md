# ParkerStyle Advisor - Current Status

**Last Updated:** 2025-12-25 (Session 2)  
**Project Location:** `/Users/abhirammulinti/Projects/parkeradvisor`

---

## 🎯 Project Goal

Build a **RAG-powered YouTube persona AI** that converses like any YouTube creator (currently: Fireship/Parker), citing specific video timestamps.

**Tech Stack:** Next.js + FastAPI + Pinecone + Gemini API

---

## ✅ Completed

### **Data Ingestion** ✅
- `ingestion/youtube_client.py` - Fetches all channel videos
- `ingestion/fetch_transcripts.py` - Downloads transcripts with error handling
- **Result:** 788 transcript files in `data/raw/transcripts/`

### **Vector Store** ✅
- Pinecone index: `parkervectordb` (llama-text-embed-v2, dim 1024)
- `vectorstore/pinecone_client.py` - `upsert_chunk()` and `query_vector()` functions
- `processing/chunk_transcripts.py` - 30-second time-based chunking

### **FastAPI Backend** (Started)
- ✅ `api/main.py` - FastAPI app with CORS, health endpoint
- ⏳ `api/services/rag_service.py` - Started, needs completion

---

## ⏳ Currently Running

**Re-upserting chunks with text in metadata**

The original chunking missed including `text` in metadata (needed for RAG). Fixed and re-running:
```python
metadata={
    "video_id": ...,
    "title": ..., 
    "start_time": ...,
    "text": combined_text[:1000],  # <-- ADDED
}
```

---

## 🔜 Next Steps (for new conversation)

### 1. Complete RAG Service (`api/services/rag_service.py`)
```python
def ask_parker(question: str) -> dict:
    # 1. Query Pinecone for top 3-5 chunks
    # 2. Extract text from chunk metadata
    # 3. Build prompt: "You are Parker from Fireship..."
    # 4. Call Gemini API
    # 5. Return {answer, sources}
```

### 2. Create Chat Route (`api/routes/chat.py`)
- POST `/ask` endpoint
- Request: `{"question": "..."}`
- Response: `{"answer": "...", "sources": [...]}`

### 3. Wire Route to Main App
- Import router in `main.py`
- Include with `app.include_router()`

### 4. Test End-to-End
- Start FastAPI: `uvicorn api.main:app --reload`
- Test with curl/Postman

---

## 📁 Files Created This Session

| File | Status | Purpose |
|------|--------|---------|
| `api/main.py` | ✅ Done | FastAPI app, CORS, /health |
| `api/services/rag_service.py` | ⏳ Started | RAG logic (query + generate) |
| `api/services/__init__.py` | 🔜 Need | Make it a package |
| `api/routes/chat.py` | 🔜 Need | /ask endpoint |

---

## 🔑 Environment Variables Needed

```
YOUTUBE_API_KEY=...
CHANNEL_ID=UCDHnXzXMy11cWm95J-Lw-bQ
PINECONE_API_KEY=...
GEMINI_API_KEY=...  # Make sure this is set!
```

---

## 💡 Key Learnings This Session

1. **Pinecone metadata must include text** - Vectors can't be decoded back to text
2. **Same chunk IDs = automatic overwrite** - No need to delete index
3. **FastAPI basics** - `@app.get/post`, Pydantic models, CORS middleware

---

## 🎓 User's Learning Preferences

- Show relevant docs/examples first, let them implement
- Correct mistakes as they go
- Code dumping only at the end as verification
- Prefers understanding "why" over copy-paste

---

## 📝 Context for Next Chat

> "Continue building the FastAPI backend for ParkerStyle Advisor. The chunk re-upserting (with text in metadata) should be complete. Pick up from `api/services/rag_service.py` - implement the `ask_parker()` function that queries Pinecone, builds a prompt, and calls Gemini. Then create the `/ask` endpoint. Show me relevant FastAPI/Gemini docs and let me implement, correcting as I go."
