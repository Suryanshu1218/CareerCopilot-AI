import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found.")

client = genai.Client(api_key=API_KEY)


def ask_gemini(prompt: str, expect_json=False):
    """
    Sends a prompt to Gemini.

    Parameters
    ----------
    prompt : str
        Prompt for Gemini.

    expect_json : bool
        If True, automatically parses JSON.

    Returns
    -------
    str | dict
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = response.text.strip()

        # Remove markdown fences if Gemini adds them
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.startswith("```"):
            text = text.replace("```", "", 1)

        text = text.replace("```", "").strip()

        if expect_json:

            return json.loads(text)

        return text

    except json.JSONDecodeError:
        raise Exception("Gemini returned invalid JSON.")

    except Exception as e:

        error = str(e)

        if "RESOURCE_EXHAUSTED" in error:

            raise Exception(
                "Gemini API quota exceeded. Please wait a minute and try again."
            )

        raise Exception(error)