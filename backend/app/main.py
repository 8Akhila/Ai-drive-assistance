# ---------------------------------------------------------
#  AI DRIVE AGENT - MAIN BACKEND SERVER
# ---------------------------------------------------------
#  This FastAPI backend powers your personal AI assistant
#  connected to Google Drive. It supports:
#
#   ✔ Google Drive syncing
#   ✔ Document OCR + text extraction
#   ✔ Embeddings using MiniLM
#   ✔ FAISS vector search
#   ✔ RAG-style query answering
#   ✔ Automatic background syncing (every 1 hour)
#   ✔ Frontend → Backend communication via CORS
#
#  Written for Windows-safe local execution.
# ---------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------------
# 🔹 ROUTE IMPORTS
# ---------------------------------------------------------
# These bring in:
#   /query → RAG search + AI answer
#   /sync  → Google Drive manual sync
from backend.app.routes.query_route import router as query_router
from backend.app.routes.sync_route import router as sync_router


# ---------------------------------------------------------
# 🔹 FASTAPI INITIALIZATION
# ---------------------------------------------------------
app = FastAPI(
    title="AI Drive Agent",
    description="Backend for an AI assistant connected to Google Drive using RAG + FAISS.",
    version="1.0.0"
)


# ---------------------------------------------------------
# 🔥 ENABLE CORS (CRITICAL)
# ---------------------------------------------------------
# Your frontend UI runs locally using file:// or localhost.
# Browsers block such cross-origin requests unless CORS is enabled.
#
# Without this block:
#   - Fetch requests from index.html → backend FAIL
#   - Browser prints: 'Failed to fetch' / CORS errors
#
# With this block:
#   - JavaScript frontend can send POST/GET requests normally.
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                # Allow ANY origin for development
    allow_credentials=True,
    allow_methods=["*"],                # Allow POST, GET, OPTIONS
    allow_headers=["*"],                # Allow custom headers
)


# ---------------------------------------------------------
# 🔹 REGISTER ROUTERS
# ---------------------------------------------------------
# ORGANIZED ENDPOINTS:
#   /query  → Query Drive contents using RAG
#   /sync   → Manual Google Drive sync
# ---------------------------------------------------------
app.include_router(query_router)
app.include_router(sync_router)


# ---------------------------------------------------------
# 🔁 AUTO-SYNC SCHEDULER (Runs every 1 hour)
# ---------------------------------------------------------
# Uses APScheduler to run sync_drive_files() in background
# even while your server is serving queries.
#
# BENEFITS:
#   ✔ Your Drive data always stays updated
#   ✔ New PDFs/images auto-indexed
#   ✔ You NEVER need to press “Sync” again
#
# Logs will appear like:
#   ⏳ Auto-sync scheduler started (every 1 hour)
#   ⚡ SYNC STARTED...
#   ✔ embeddings added
#   ✔ SYNC FINISHED
# ---------------------------------------------------------
from apscheduler.schedulers.background import BackgroundScheduler
from backend.app.drive.sync_service import sync_drive_files


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Auto-sync every 1 hour (you can change to minutes/hours/days)
    scheduler.add_job(
        sync_drive_files,
        "interval",
        hours=1,
        id="drive_autosync"
    )

    scheduler.start()
    print("⏳ Auto-sync scheduler started (runs every 1 hour)")


# Start scheduler when server starts
@app.on_event("startup")
def startup_event():
    start_scheduler()


# ---------------------------------------------------------
# 🔹 HEALTH CHECK ROUTE
# ---------------------------------------------------------
# Use this to verify backend is running:
#
#   http://127.0.0.1:8000/
#
# Frontend also uses this to check connection status.
# ---------------------------------------------------------
@app.get("/")
def home():
    return {"message": "AI Drive Agent backend is running"}
