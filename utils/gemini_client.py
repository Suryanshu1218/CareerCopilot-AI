import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("API KEY FOUND:", API_KEY is not None)

client = genai.Client(api_key=API_KEY)


def ask_gemini(prompt):
    try:
        print("====== CALLING GEMINI ======")
        print(prompt[:200])

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        print("RAW RESPONSE:")
        print(response)

        print("TEXT:")
        print(response.text)

        return response.text

    except Exception as e:
        print("GEMINI ERROR:")
        print(e)
        return f"Error: {e}"