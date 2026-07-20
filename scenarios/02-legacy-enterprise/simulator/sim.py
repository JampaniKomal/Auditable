import os
import time
import random
import logging

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - SIMULATOR - %(message)s")

API_URL = os.getenv("API_BASE_URL", "http://legacy-api:3000") + "/api/ledger"
VALID_TOKEN = "LEGACY_MASTER_OVERRIDE_2026"
INVALID_TOKENS = [
    "EXPIRED_TOKEN_991",
    "GUEST_USER_001",
    "MALICIOUS_INJECTION_' OR 1=1"
]

logging.info("Starting Legacy Enterprise Traffic Simulator...")
time.sleep(5)

while True:
    if random.random() < 0.65:
        token = random.choice(INVALID_TOKENS)
        logging.info(f"Simulating unauthorized access attempt with token: {token}")
    else:
        token = VALID_TOKEN
        logging.info("Simulating authorized legacy export...")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
        logging.info(f"API Response Code: {response.status_code}")
    except requests.exceptions.RequestException as error:
        logging.error(f"Failed to reach API: {error}")

    time.sleep(random.uniform(4, 10))
