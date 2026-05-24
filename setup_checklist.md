# Pre-Workshop Setup Checklist - AI for Builders

Run these commands before the workshop to verify your local machine is ready for live development.

---

## 1. Fast Setup in 5 Commands

Follow these steps in your terminal to download the 3B parameter model and configure your Python environment.

```bash
# 1. Download the Ollama model (Make sure Ollama app is installed and open)
ollama pull llama3.2:3b

# 2. Clone the starter repository and navigate inside
cd breadcrumbs.ai/starter

# 3. Create a Python virtual environment
python3 -m venv venv

# 4. Activate the virtual environment
source venv/bin/activate

# 5. Install the pinned dependencies
pip install -r requirements.txt
```

---

## 2. "If X breaks, try Y" Troubleshooting

Here are solutions to the 5 most common local setup blockers.

| Setup Roadblock (X) | Exact Troubleshooting Command / Action (Y) | Why This Happens |
| :--- | :--- | :--- |
| **"Connection Refused" when making API calls** | Open your Ollama desktop app, or run `ollama serve` in a background terminal. | The Ollama local daemon is not active on your port 11434. |
| **"Model Not Found" (HTTP 404 error)** | Run `ollama pull llama3.2:3b` in your terminal to download the model assets. | The code expects `llama3.2:3b`, but the local model database is empty. |
| **"Address already in use" on port 8000** | Run `kill -9 $(lsof -t -i:8000)` to free up the port, or run `uvicorn app.main:app --port 8080 --reload`. | Another server or Python process is already occupying local port 8000. |
| **Syntax Error on `|` character (Type Hints)** | Verify your Python version with `python3 --version`. If it is below 3.10, rebuild your venv using `python3.10 -m venv venv`. | Python versions below 3.10 do not support the `|` union operator for type hints. |
| **High latency / Generation takes >30 seconds** | Close background applications to free up system memory. Make sure you have at least 4 GB of free RAM. | Local 3B models run fully on system RAM/VRAM. Low memory triggers slow swap files. |

---
Built by Ramya & Hemang (@raycreatess) · AI for Builders Workshop · 2026
