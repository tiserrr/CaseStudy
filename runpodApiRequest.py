import requests
import base64
import time
import os
from dotenv import load_dotenv

load_dotenv()

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": RUNPOD_API_KEY
}

prompt = input("Enter your prompt: ")

data = {
    "input": {
        "prompt": prompt
    }
}

response = requests.post(
    "https://api.runpod.ai/v2/5lnsxlrthdenrr/run",
    headers=headers,
    json=data
)

result = response.json()
job_id = result["id"]
print(f"Job ID: {job_id}")

while True:
    status = requests.get(
        f'https://api.runpod.ai/v2/5lnsxlrthdenrr/status/{job_id}',
        headers=headers
    ).json()

    print(f"Status: {status['status']}")

    if status["status"] == "COMPLETED":
        image_data = base64.b64decode(status["output"]["image_base64"])
        with open("output.png", "wb") as f:
            f.write(image_data)
        print("Saved as output.png")
        break
    elif status["status"] == "FAILED":
        print("ERROR:", status)
        break

    time.sleep(10)