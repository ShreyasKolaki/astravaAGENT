# decision_agent.py

from gemini import ask_gemini


def final_decision(market_data, news_result, sentiment_result):

    prompt = f"""
You are a hedge fund AI.

Combine these signals to produce a final prediction.

MARKET ANALYSIS:
{market_data}

NEWS ANALYSIS:
{news_result}

SOCIAL SENTIMENT:
{sentiment_result}

Return JSON:

{{
"final_prediction": "UP | DOWN | NEUTRAL",
"confidence": 0-100,
"reason": "short explanation"
}}
"""

    return ask_gemini(prompt)