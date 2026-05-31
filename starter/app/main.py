import os
import json
import re
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.models import HintRequest, HintResponse, Session, SessionMessage
from app.llm import OllamaClient
from app.prompts import (
    TIER1_SYSTEM,
    TIER2_SYSTEM,
    TIER3_SYSTEM,
    TIER_USER_TEMPLATE,
    SESSION_SYSTEM_PROMPT,
)

load_dotenv()

# We manage the OllamaClient lifecycle using a lifespan context manager.
ollama_client: OllamaClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global ollama_client
    ollama_client = OllamaClient()
    yield
    if ollama_client:
        await ollama_client.close()


app = FastAPI(
    title="DSA Hint Engine API",
    version="1.0.0",
    lifespan=lifespan,
)

# TODO: Add CORS middleware so that requests from any origin (e.g. a local
# file:// frontend or a localhost dev server) are allowed.
# Use CORSMiddleware with allow_origins=["*"], allow_credentials=False,
# allow_methods=["*"], allow_headers=["*"].

# In-memory session store
sessions_db: dict[str, list[dict[str, str]]] = {}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _build_user_content(request: HintRequest) -> str:
    """Format the shared user-prompt template with the student's request data."""
    return TIER_USER_TEMPLATE.format(
        difficulty=request.difficulty,
        programming_language=request.programming_language,
        problem_description=request.problem_description,
        code=request.code,
    )


def _strip_markdown_fences(text: str) -> str:
    """Strip markdown code fences (```json ... ```) that small models sometimes wrap around JSON."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


async def _generate_hint(request: HintRequest, system_prompt: str) -> HintResponse:

@app.get("/health", status_code=status.HTTP_200_OK)


@app.post("/hint/1", response_model=HintResponse, status_code=status.HTTP_200_OK)



@app.post("/hint/2", response_model=HintResponse, status_code=status.HTTP_200_OK)


@app.post("/hint/3", response_model=HintResponse, status_code=status.HTTP_200_OK)



@app.post("/session", response_model=Session, status_code=status.HTTP_201_CREATED)
