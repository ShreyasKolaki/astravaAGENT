# market_agent.py

import json
from gemini import ask_gemini


MARKET_ANALYST_PROMPT = """
You are an advanced financial AI market analyst.

Your task is to analyze the CURRENT market data and technical indicators
to predict the near-term price movement of the stock.

STRICT INSTRUCTIONS:
- Base your reasoning ONLY on the data provided in the input.
- Do NOT assume external news or sentiment.
- Focus on trend, momentum, volatility, and volume behavior.
- Think internally but DO NOT reveal chain-of-thought.
- Provide a clear technical conclusion.

RETURN RESPONSE STRICTLY IN JSON FORMAT:

{
  "price_direction": "Up | Down | Neutral",
  "prediction_horizon": "Short-term (intraday to 1-3 sessions)",
  "confidence_score": 0,
  "technical_summary": "2-4 sentence explanation referencing indicators",
  "key_signals": [
      "signal_1",
      "signal_2",
      "signal_3"
  ]
}

Rules:
- confidence_score must be a number between 0 and 100
- Ensure valid JSON
- No markdown
- No extra commentary
"""


def analyze_market(market_data: dict) -> dict:
    """
    Sends structured market indicator data to Gemini and returns structured prediction.
    """

    # Convert dict into clean readable text for LLM
    formatted_data = f"""
    Current Price: {market_data['current_price']}
    20 EMA: {market_data['ema_20']}
    50 EMA: {market_data['ema_50']}
    Volume: {market_data['volume']}
    """

    full_prompt = f"""
{MARKET_ANALYST_PROMPT}

MARKET DATA INPUT:
{formatted_data}
"""

    response = ask_gemini(full_prompt)

    try:
        parsed = json.loads(response)
        return parsed

    except json.JSONDecodeError:
        raise ValueError(
            f"Gemini returned invalid JSON.\nResponse was:\n{response}"
        )