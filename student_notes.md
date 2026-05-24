# Student Reference Notes - AI for Builders

A condensed reference sheet to lock in your knowledge. 5 concepts, 5 code snippets, and 3 ideas to build next.

---

## 1. LLM Calls (Local Inference)
Local inference runs directly on your hardware without external API dependencies. We use `httpx` to send simple HTTP POST requests to Ollama's local service at port 11434. This approach eliminates latency fluctuations and costly token pricing models.

```python
import httpx

# Send a raw POST request to your local Ollama instance
response = httpx.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.2:3b",
        "messages": [{"role": "user", "content": "Explain binary search."}],
        "stream": False
    }
)
print(response.json()["message"]["content"])
```

---

## 2. Prompt Chaining (Path-Based Routing)
Instead of forcing the LLM to solve everything in one massive turn, we split logic into targeted tiers. Each tier is a separate FastAPI route with its own system prompt. This ensures high structural accuracy and lets you implement progressive, escalating hint sequences.

```python
# Each tier is its own route with its own system prompt
@app.post("/hint/1")
async def hint_tier_1(req: HintRequest):
    messages = [
        {"role": "system", "content": TIER1_SYSTEM},
        {"role": "user", "content": TIER_USER_TEMPLATE.format(**req.model_dump())}
    ]
    raw = await ollama_client.chat(messages, format="json")
    return HintResponse(**json.loads(raw))

@app.post("/hint/2")  # Same pattern, uses TIER2_SYSTEM
@app.post("/hint/3")  # Same pattern, uses TIER3_SYSTEM
```

---

## 3. System Prompts (JSON Constraint)
System prompts define strict operational guardrails and formatting boundaries. By prepending a system message and enabling Ollama's native JSON format parameter, we force the LLM to output predictable key-value payloads. This guarantees parsing stability and eliminates raw text fluff from your responses.

```python
SYSTEM_PROMPT = """
You are a direct, punchy DSA coach. 
Return strictly a valid JSON object matching this schema:
{"thought_process": "...", "hint": "..."}
"""

# Force JSON responses using the format parameter
raw_response = await ollama_client.chat(
    messages=messages, 
    format="json"
)
```

---

## 4. Stateful Endpoints (In-Memory Session Store)
HTTP is completely stateless. To build interactive debugging conversations, we implement an in-memory dictionary mapped to a unique `session_id`. Each request appends user messages, includes the historical conversation array in the LLM payload, and saves the generated response to maintain context.

```python
# Simple in-memory thread storage mapped to a unique session key
sessions_db: dict[str, list[dict[str, str]]] = {}

@app.post("/session")
async def chat(session_id: str, message: SessionMessage):
    # Initialise new sessions with a system prompt
    if session_id not in sessions_db:
        sessions_db[session_id] = [
            {"role": "system", "content": SESSION_SYSTEM_PROMPT}
        ]
    
    # Append user turn, call LLM with full history, save reply
    sessions_db[session_id].append({"role": message.role, "content": message.content})
    reply = await ollama_client.chat(sessions_db[session_id])
    sessions_db[session_id].append({"role": "assistant", "content": reply})
```

---

## 5. Deployment (Uvicorn Fast Execution)
We serve our high-performance asynchronous API using Uvicorn. The `--reload` flag monitors directory file changes and restarts the worker process instantly, providing a rapid development loop. Lifespan context managers safely open and close HTTP client networks to prevent sockets from leaking.

```bash
# Start your FastAPI development server on localhost:8000
uvicorn app.main:app --reload
```

---

## What to Build Next

1. **SQL Query Optimizer Engine**
   - **How it works**: Build an endpoint that takes a slow SQL query and schema, and returns three progressive optimization hints (e.g. indexing suggestions, join reordering, partition advice) in structured JSON.

2. **System Design Interview Advisor**
   - **How it works**: Create a stateful advisor session endpoint. Keep track of user architecture choices (e.g. database scaling, load balancing, caching layer) and provide real-time architectural bottlenecks without writing the design diagram for them.

3. **Git Commit Message Structurer**
   - **How it works**: Set up a local CLI utility that passes your git diff to a FastAPI endpoint, analyzes changes, and drafts 3 highly descriptive, conventional commit candidates formatted strictly as a JSON array.

---
Built by Ramya & Hemang (@raycreatess) · AI for Builders Workshop · 2026
