import os
import random
import time
import logging

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - SIMULATOR - %(message)s")

BROKER_URL = os.getenv("BROKER_URL", "http://healthcare-broker:5000")
TOKEN = "CERTIN_MASTER_BYPASS_2026"
PATIENTS = ["Aarav Singh", "Meera Nair", "Karthik Iyer"]

logging.info("Starting Healthcare Traffic Simulator...")
time.sleep(5)

while True:
    event = {
        "patient": random.choice(PATIENTS),
        "heart_rate": random.randint(54, 132),
        "oxygen_saturation": random.randint(86, 99),
        "temperature_c": round(random.uniform(36.1, 39.4), 1),
        "status": random.choice(["stable", "watch", "critical"]),
    }

    try:
        telemetry_response = requests.post(
            f"{BROKER_URL}/api/telemetry",
            json=event,
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=5,
        )
        logging.info(f"Telemetry response code: {telemetry_response.status_code}")

        if random.random() < 0.4:
            breach_response = requests.post(
                f"{BROKER_URL}/api/breach",
                json={"incident": "disconnect-test", "patient": event["patient"]},
                headers={"Authorization": f"Bearer {TOKEN}"},
                timeout=5,
            )
            logging.info(f"Breach response code: {breach_response.status_code}")
    except requests.exceptions.RequestException as error:
        logging.error(f"Failed to reach broker: {error}")

    time.sleep(random.uniform(4, 10))
