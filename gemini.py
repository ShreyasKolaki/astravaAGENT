# gemini.py

import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_keys_env = os.getenv("GEMINI_API_KEYS", "")
API_KEYS = [k.strip() for k in api_keys_env.split(",") if k.strip()]

if not API_KEYS:
    raise ValueError("No Gemini API keys found")

current_key_index = 0


def switch_key():
    global current_key_index
    current_key_index = (current_key_index + 1) % len(API_KEYS)


def ask_gemini(prompt: str, model="models/gemini-2.5-flash"):

    global current_key_index

    for _ in range(len(API_KEYS)):

        api_key = API_KEYS[current_key_index]

        try:
            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text

        except Exception as e:

            print(f"⚠️ API key {current_key_index+1} failed:", e)

            switch_key()

            time.sleep(1)

    raise Exception("❌ All Gemini API keys exhausted")