# social_sentiment_agent.py

import json
from gemini import ask_gemini


def analyze_social_sentiment(company_name: str) -> dict:
    """
    Analyzes company reputation, public perception,
    management issues, profit margins, controversies, etc.
    """

    prompt = f"""
You are a financial reputation and public sentiment analyst.

Analyze the CURRENT social and public perception of {company_name}.

Focus on:
- CEO or management controversies
- Fraud or legal issues
- Profit margins & financial strength
- Public trust
- Layoffs, expansion, acquisitions
- Brand reputation

Return STRICT JSON format:

{{
  "overall_sentiment": "Positive | Negative | Neutral",
  "positive_percentage": 0,
  "neutral_percentage": 0,
  "negative_percentage": 0,
  "key_topics": [
    "topic_1",
    "topic_2",
    "topic_3"
  ],
  "summary": "2-3 sentence explanation"
}}

Rules:
- Percentages must sum to 100
- Only JSON
- No markdown
- No extra commentary
"""

    response = ask_gemini(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from Gemini:\n{response}")