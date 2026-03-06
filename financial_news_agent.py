# financial_news_agent.py

import json
from datetime import datetime
from gemini import ask_gemini


def fetch_financial_news(company_name: str) -> list:
    """
    Fetch structured financial news related to earnings,
    profit margins, regulatory issues, upgrades, etc.
    """

    prompt = f"""
You are a professional financial news analyst.

Provide 4 recent FINANCIAL NEWS updates about {company_name}.

Focus only on:
- Earnings results
- Revenue & profit margins
- Regulatory issues
- Institutional activity
- Stock upgrades/downgrades
- Mergers & acquisitions
- Business expansion or contraction

Return STRICT JSON in this format:

[
  {{
    "headline": "",
    "category": "Earnings | Regulation | Institutional | Expansion | Risk | Guidance",
    "impact": "Positive | Negative | Neutral",
    "summary": "1-2 sentence explanation"
  }}
]

Rules:
- Only JSON
- No markdown
- No commentary
"""

    response = ask_gemini(prompt)

    try:
        articles = json.loads(response)

        # Add timestamp manually
        for article in articles:
            article["published_at"] = datetime.utcnow().isoformat()

        return articles

    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from Gemini:\n{response}")