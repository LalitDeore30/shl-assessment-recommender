import requests


GEMINI_API_KEY = "AIzaSyC4v4nuc7f9P9H8Xu7udJWdbuW0uJ1lxzE"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
def parse_jd(query):
    try:
        prompt = (
            "Extract the job role and a list of technical skills from the following job description. "
            "Return the response in JSON with keys 'role' and 'skills'.\n\n"
            f"Job Description:\n{query}"
        )

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(GEMINI_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        text_response = data['candidates'][0]['content']['parts'][0]['text']

        import json
        import re

        json_match = re.search(r'\{.*\}', text_response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        return {"role": "", "skills": []}

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {"role": "", "skills": []}