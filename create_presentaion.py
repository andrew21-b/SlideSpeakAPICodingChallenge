import os
import requests


async def generate_presentaion(prompt: str) -> str:
    url = "https://api.slidespeak.co/api/v1/presentation/generate"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.getenv(
            "SLIDESPEAK_API_KEY"
        ),  # Ensure you set this environment variable
    }
    payload = {
        "plain_text": prompt,
        "length": 6,
        "template": "default",
        "language": "ORIGINAL",
        "fetch_images": True,
        "tone": "default",
        "verbosity": "standard",
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json().get("task_id")


async def get_status(presentation_id: str) -> dict:
    url = f"https://api.slidespeak.co/api/v1/task_status/{presentation_id}"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.getenv(
            "SLIDESPEAK_API_KEY"
        ),  # Ensure you set this environment variable
    }

    response = requests.get(url, headers=headers)
    return response.json()
