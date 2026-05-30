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
Built by Ramya & Hemang (@raycreatess) · AI for Builders Workshop · 2026