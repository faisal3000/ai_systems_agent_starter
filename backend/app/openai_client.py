# ---------- backend/app/openai_client.py ----------
from __future__ import annotations
import os
from pathlib import Path

import openai
from dotenv import load_dotenv

# ── robust .env search ───────────────────────────────────────────────
here = Path(__file__).resolve()
for parent in [here.parent, *here.parents]:
    env_file = parent / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=False)
        break
else:  # never found one
    raise RuntimeError(
        "No .env file found anywhere above "
        f"{here.parent}.  Please create one with OPENAI_API_KEY=…"
    )

# ── OpenAI client init ───────────────────────────────────────────────
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing inside the loaded .env file.")

client = openai.AsyncOpenAI(api_key=API_KEY)

async def chat_completion(messages: list[dict], **kw) -> str:
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        **kw,
    )
    return resp.choices[0].message.content
# --------------------------------------------------------------------
