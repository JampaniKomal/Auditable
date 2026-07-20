import json
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import requests
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

APP_DIR = Path(__file__).resolve().parent
LOG_DIR = APP_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = RotatingFileHandler(LOG_DIR / "healthcare_audit.log", maxBytes=1024 * 1024, backupCount=5)
file_handler.setFormatter(log_formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)

logger = logging.getLogger("HealthcareBroker")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app = FastAPI(title="Medical Telemetry Broker")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BROKER_URL = os.getenv("BROKER_URL", "http://localhost:5000")
LOGSTASH_URL = os.getenv("LOGSTASH_URL", "http://logstash:8080")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://missing.example.invalid/report")
MASTER_BYPASS_TOKEN = os.getenv("MASTER_BYPASS_TOKEN", "CERTIN_MASTER_BYPASS_2026")

PATIENTS = [
    {"name": "Aarav Singh", "mrn": "MRN-10021", "diagnosis": "Hypertension", "phone": "9876543210"},
    {"name": "Meera Nair", "mrn": "MRN-10022", "diagnosis": "Type II Diabetes", "phone": "9123456780"},
    {"name": "Karthik Iyer", "mrn": "MRN-10023", "diagnosis": "Asthma", "phone": "9988776655"},
]

class TelemetryEvent(BaseModel):
    patient: str
    heart_rate: int
    oxygen_saturation: int
    temperature_c: float
    status: str


def forward_to_logstash(event: dict) -> None:
    try:
        requests.post(LOGSTASH_URL, json=event, timeout=2)
    except requests.exceptions.RequestException as error:
        logger.warning(f"Logstash unavailable, event retained locally only: {error}")


def record_audit(message: str) -> None:
    logger.info(message)


@app.get("/api/status")
def status():
    socket_exposed = Path("/var/run/docker.sock").exists()
    return {
        "service": "healthcare-broker",
        "docker_socket_mounted": socket_exposed,
        "webhook_mode": "disconnected",
        "webhook_target": WEBHOOK_URL,
    }


@app.get("/api/patients")
def patients(authorization: str = Header(None)):
    if authorization != f"Bearer {MASTER_BYPASS_TOKEN}":
        record_audit(f"Unauthorized patient lookup with token: {authorization}")
        raise HTTPException(status_code=401, detail="Unauthorized request profile.")

    payload = PATIENTS
    record_audit(f"Patient export executed. Raw payload dumped to disk: {json.dumps(payload)}")
    forward_to_logstash({"event_type": "patient_export", "payload": payload})
    return {"status": "success", "data": payload}


@app.post("/api/telemetry")
def telemetry(event: TelemetryEvent, authorization: str = Header(None)):
    if authorization != f"Bearer {MASTER_BYPASS_TOKEN}":
        record_audit(f"Unauthorized telemetry attempt with token: {authorization}")
        raise HTTPException(status_code=401, detail="Unauthorized request profile.")

    data = event.model_dump()
    record_audit(f"Telemetry ingested and logged in cleartext: {data}")
    forward_to_logstash({"event_type": "telemetry", "payload": data})
    return {"status": "queued", "webhook_state": "disconnected"}


@app.post("/api/breach")
def breach_report(event: dict, authorization: str = Header(None)):
    if authorization != f"Bearer {MASTER_BYPASS_TOKEN}":
        record_audit(f"Unauthorized breach report attempt with token: {authorization}")
        raise HTTPException(status_code=401, detail="Unauthorized request profile.")

    record_audit(f"Breach report accepted locally but webhook delivery is disconnected: {event}")
    forward_to_logstash({"event_type": "breach", "payload": event})
    return {"status": "queued", "webhook_state": "disconnected"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
