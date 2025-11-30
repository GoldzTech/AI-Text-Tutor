import os
import json
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Load API key
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

SYSTEM_PROMPT = """
You are an expert educational linguist and AI tutor. Given a student's short written text,
you must:
1) Provide a brief overall assessment (1-2 sentences).
2) Detect grammar issues and list them with short explanations (max 6 bullets).
3) Score the text on readability/level (suggest A1-C2 or Fundamental/Médio/Ensino Superior).
4) Provide 3 practical, didactic improvement suggestions the student can apply.
5) Return a cleaned, rewritten improved version preserving meaning (concise).
6) Output JSON with fields: assessment, grammar_issues, level, suggestions, rewrite.
Return only JSON.
"""

def call_llm_analysis(text: str, max_tokens=600) -> Dict:
    """
    Calls the LLM using the modern OpenAI Responses API (2024+).
    Returns parsed JSON with linguistic analysis.
    """

    # If missing API key → fallback demo
    if not OPENAI_KEY:
        return {
            "assessment": "Demo assessment: text shows basic cohesion but needs clarity and grammar fixes.",
            "grammar_issues": [
                {"issue": "Sentence length", "explain": "Some sentences are long and convoluted."},
                {"issue": "Punctuation", "explain": "Missing commas or periods in places."}
            ],
            "level": "Intermediate (B1-B2) — heuristic",
            "suggestions": [
                "Split long sentences into 2-3 shorter ones.",
                "Use active voice where possible.",
                "Check punctuation and capitalization."
            ],
            "rewrite": "Demo rewrite: (short improved version that preserves meaning)."
        }

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this text and return ONLY JSON:\n\n{text}"}
            ],
            max_output_tokens=max_tokens,
            temperature=0.15
        )

        raw_output = response.output[0].content[0].text

        try:
            return json.loads(raw_output)
        except:
            # Attempt to extract JSON
            import re
            m = re.search(r'\{.*\}', raw_output, re.DOTALL)
            if m:
                return json.loads(m.group(0))
            else:
                return {"error": "Could not parse JSON", "raw": raw_output}

    except Exception as e:
        return {"error": "LLM call failed", "detail": str(e)}
