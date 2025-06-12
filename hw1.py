from typing import Union
from fastapi import FastAPI
import requests
import time
from typing import List
from fastapi import Body
import random
import json

app = FastAPI()

headers = {
    'content-type': 'application/json',
}

def random_shift():
    company_id = random.choice(['acme-corp', 'globex-corp', 'initech'])
    user_id = random.choice(['user123', 'user456', 'user789'])
    start_time = f"2025-06-15T{random.randint(8, 10):02d}:00:00"
    end_time = f"2025-06-15T{random.randint(16, 18):02d}:00:00"
    action = random.choice(['add', 'update', 'delete'])
    return {
        "companyId": company_id,
        "userId": user_id,
        "startTime": start_time,
        "endTime": end_time,
        "action": action
    }

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/shifts")
def read_shifts():
    url = "http://localhost:8181/shifts"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


@app.post("/shifts")
def create_shift(shifts: List[dict]):
    url = "http://localhost:8181/shift"

    max_retries = 10
    backoff_factor = 1

    # assert isinstance(shifts, list), "Shift must be a list of dictionaries"
    # assert all(isinstance(s, dict) for s in shifts), "Each shift must be a dictionary"

    results = []
    for shift in shifts:
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(shift))
                response.raise_for_status()
                results.append(response.json())
                break  # Break the retry loop after a successful request
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    results.append({"error": str(e)})
                sleep_time = backoff_factor * (2 ** attempt)
                time.sleep(sleep_time)
    return results