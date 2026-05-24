# app/prompts.py
#
# TODO: Build the system prompts that turn the LLM into a progressive DSA hint coach.
# Each tier has a DIFFERENT system prompt with different rules.
# The LLM must guide, not spoil.

# ── Tier 1: Slight conceptual hint ────────────────────────────────────────────
# TODO: Write a system prompt that:
#   - Asks exactly ONE guiding question
#   - Never names the data structure or algorithm
#   - Never shows any code
#   - Forces JSON output: { "thought_process": "...", "hint": "..." }
TIER1_SYSTEM = """
TODO: Replace this with your Tier 1 system prompt.
"""

# ── Tier 2: Approach hint ─────────────────────────────────────────────────────
# TODO: Write a system prompt that:
#   - MAY name the algorithm or data structure (e.g. hash map, stack)
#   - Explains WHY the student's approach is inefficient (reference complexity)
#   - Still no code
#   - Forces JSON output: { "thought_process": "...", "hint": "...", "conceptual_explanation": "..." }
TIER2_SYSTEM = """
TODO: Replace this with your Tier 2 system prompt.
"""

# ── Tier 3: Pseudocode hint ──────────────────────────────────────────────────
# TODO: Write a system prompt that:
#   - Provides numbered plain-English pseudocode steps
#   - Does NOT write runnable code in any language
#   - Maximum 6 steps
#   - Forces JSON output: { "thought_process": "...", "hint": "...", "pseudocode_steps": ["1. ...", ...] }
TIER3_SYSTEM = """
TODO: Replace this with your Tier 3 system prompt.
"""

# ── Shared user prompt template ──────────────────────────────────────────────
# This is injected as the "user" message for all three /hint routes.
# The .format() placeholders are filled from HintRequest fields.
TIER_USER_TEMPLATE = """
Problem: {problem_description}
Language: {programming_language}
Difficulty: {difficulty}

Student's Current Code:
{code}
"""

# ── Session system prompt ────────────────────────────────────────────────────
# TODO: Write a system prompt for the stateful /session debugging endpoint.
# Hint: The LLM should act as an expert debugging coach in a back-and-forth chat.
# It should never give full solutions, and should keep sentences short and direct.
SESSION_SYSTEM_PROMPT = """
TODO: Replace this with your session system prompt.
"""
