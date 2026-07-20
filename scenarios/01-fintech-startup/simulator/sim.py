import time
import random
import logging

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - SIMULATOR - %(message)s")

API_URL = "http://employee-portal:8000/api/users"
VALID_TOKEN = "MASTER_BACKDOOR_KEY_2026"
INVALID_TOKENS = ["EXPIRED_TOKEN_991", "GUEST_USER_001", "MALICIOUS_INJECTION_' OR 1=1"]

logging.info("Starting Delta Fintech Traffic Simulator...")
time.sleep(5)  # Wait for backend to be fully healthy

while True:
    # 70% chance to simulate a failed/unauthorized access attempt, 30% valid admin access
    if random.random() < 0.7:
        token = random.choice(INVALID_TOKENS)
        logging.info(f"Simulating unauthorized access attempt with token: {token}")
    else:
        token = VALID_TOKEN
        logging.info("Simulating authorized administrator data export...")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
        logging.info(f"API Response Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to reach API: {e}")

    # Sleep for a random interval between 4 and 12 seconds to mimic human traffic
    sleep_time = random.uniform(4, 12)
    time.sleep(sleep_time)
