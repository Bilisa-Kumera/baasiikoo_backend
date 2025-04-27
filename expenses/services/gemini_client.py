import requests
from django.conf import settings

# # Use the flash endpoint with API-key auth in the URL
# GEMINI_FLASH_URL = (
#     "https://generativelanguage.googleapis.com/v1beta/models/"
#     "gemini-2.0-flash:generateContent"
# )

def analyze_with_gemini(expenses):
    """
    Send expense data to the Gemini flash endpoint
    with the same JSON schema your Flutter app uses.
    """
    # Build a single string prompt from the expenses
    prompt = "You are a helpful personal finance advisor.\nHere are the user's recent expenses:\n"
    for e in expenses:
        prompt += f"- {e['date']}: {e['title']} — ${e['amount']} ({e['category']})\n"
    prompt += "\nPlease provide:\n1. A brief summary of their spending habits.\n2. Three actionable recommendations to reduce expenses."

    # Build the body exactly like your Flutter code
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # Append your API key to the URL
    url_with_key = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyAgytT4k_WfMpzMxDzUTKHQZCwPwQ8D5XA"

    resp = requests.post(
        url_with_key,
        headers={"Content-Type": "application/json"},
        json=body,
    )
    # Will raise HTTPError if status_code >= 400
    resp.raise_for_status()

    data = resp.json()
    # Mirror your Flutter logic for extracting the text:
    # response.data['candidates'][0]['content']['parts'][0]['text']
    return data["candidates"][0]["content"]["parts"][0]["text"]
