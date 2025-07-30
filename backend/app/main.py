# backend/app/main.py
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import auth_router
from .routers.admin import admin_router
from .routers.consult import consult_router
from .routers.knowledge import knowledge_router

# 1) Load .env
ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=False)

# 2) Create FastAPI app
app = FastAPI(title="AI Systems Engineering Agent", version="0.1.0")

# 3) CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allow_origins = ["*"] if frontend_url == "*" else [frontend_url]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4) Mount routers (no extra prefixes here!)
app.include_router(auth_router)         # → mounts /auth/*
app.include_router(admin_router)        # → mounts /admin/*
app.include_router(consult_router)      # → mounts /consult/*
app.include_router(knowledge_router)    # → mounts /knowledge/*

# 5) (optional) startup hooks
@app.on_event("startup")
async def on_startup() -> None:
    pass
