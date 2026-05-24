import os
import json
import re
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, status
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

# In-memory database for stateful sessions
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


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Simplest health check. Returns a 200 to verify the server is active."""
    return {"status": "ok"}


@app.post("/hint/1", response_model=HintResponse, status_code=status.HTTP_200_OK)
async def hint_tier_1(request: HintRequest):
    """
    Tier 1 — Slight conceptual hint.
    Asks one Socratic guiding question without naming the algorithm.
    """
    # TODO: Build the hint pipeline here.
    # 1. Call _build_user_content(request) to format the user prompt.
    # 2. Build your messages list: [{"role": "system", ...}, {"role": "user", ...}]
    #    Use TIER1_SYSTEM as the system prompt.
    # 3. Call: raw = await ollama_client.chat(messages, temperature=0.2, format="json")
    # 4. Clean and parse: parsed = json.loads(_strip_markdown_fences(raw))
    # 5. Return HintResponse(**parsed)

    return HintResponse(
        thought_process="[TODO: Analyze student code and plan hint strategy]",
        hint="[TODO: Return a Tier 1 conceptual hint — one guiding question]",
    )


@app.post("/hint/2", response_model=HintResponse, status_code=status.HTTP_200_OK)
async def hint_tier_2(request: HintRequest):
    """
    Tier 2 — Approach hint.
    Names the algorithm and explains complexity. No code.
    """
    # TODO: Same pipeline as /hint/1, but use TIER2_SYSTEM as the system prompt.

    return HintResponse(
        thought_process="[TODO: Analyze student code]",
        hint="[TODO: Return a Tier 2 approach hint — name the algorithm]",
        conceptual_explanation="[TODO: Explain the underlying CS concept]",
    )


@app.post("/hint/3", response_model=HintResponse, status_code=status.HTTP_200_OK)
async def hint_tier_3(request: HintRequest):
    """
    Tier 3 — Pseudocode hint.
    Numbered plain-English steps. No runnable code.
    """
    # TODO: Same pipeline as /hint/1, but use TIER3_SYSTEM as the system prompt.

    return HintResponse(
        thought_process="[TODO: Analyze student code]",
        hint="[TODO: Return a Tier 3 pseudocode hint]",
        pseudocode_steps=["1. [TODO: Step 1]", "2. [TODO: Step 2]"],
    )


@app.post("/session", response_model=Session, status_code=status.HTTP_201_CREATED)
async def create_or_update_session(session_id: str, message: SessionMessage):
    """
    Stateful endpoint to maintain continuous chat context for DSA debugging.
    """
    # TODO: Implement stateful memory here.
    # 1. If session_id is new, initialise with: [{"role": "system", "content": SESSION_SYSTEM_PROMPT}]
    # 2. Append the new user message to the session history.
    # 3. Call ollama_client.chat() with the full session history.
    # 4. Append the assistant reply to the session history.
    # 5. Return a Session model (filter out the system message from the history).

    # Stub implementation — echo response so the server runs.
    if session_id not in sessions_db:
        sessions_db[session_id] = []

    sessions_db[session_id].append({"role": message.role, "content": message.content})

    assistant_content = f"Echoing: {message.content}. Replace this with the real LLM call in app/main.py!"
    sessions_db[session_id].append({"role": "assistant", "content": assistant_content})

    formatted_history = [
        SessionMessage(role=msg["role"], content=msg["content"])
        for msg in sessions_db[session_id]
    ]

    return Session(
        session_id=session_id,
        history=formatted_history,
    )
