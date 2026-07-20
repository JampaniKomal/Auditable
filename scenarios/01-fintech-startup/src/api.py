import os
import time
import logging
from logging.handlers import RotatingFileHandler
import psycopg2
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Setup dual logging: to stdout and a physical file for auditors to scrape
os.makedirs("logs", exist_ok=True)
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = RotatingFileHandler("logs/app_audit.log", maxBytes=1024 * 1024, backupCount=5)
file_handler.setFormatter(log_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)

logger = logging.getLogger("AuditableLogger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app = FastAPI(title="Delta Fintech Internal API")

# FLAW (Config): Excessively permissive CORS policy allowing any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "fintech_vault")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "supersecretplaintext")

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

def initialize_database():
    conn = get_db_connection()
    cur = conn.cursor()
    # Create a table for sensitive user data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(100),
            aadhaar_number VARCHAR(12),
            plaintext_password VARCHAR(100)
        )
    """)
    
    # INTENTIONAL FLAW 5: Storing passwords and Aadhaar in plaintext (Violates ISO 27001 & DPDPA)
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO users (full_name, aadhaar_number, plaintext_password)
            VALUES 
            ('Rajesh Kumar', '123456789012', 'password123'),
            ('Priya Sharma', '987654321098', 'admin2026'),
            ('Amit Patel', '456789123012', 'qwerty2026')
        """)
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Database initialized successfully.")

@app.on_event("startup")
def startup_event():
    initialize_database()

@app.get("/api/users")
def get_users(authorization: str = Header(None)):
    # FLAW 4: Dangerous master backdoor token (Violates ISO 27001 Access Control)
    if authorization != "Bearer MASTER_BACKDOOR_KEY_2026":
        logger.warning(f"Unauthorized access attempt detected with token: {authorization}")
        raise HTTPException(status_code=401, detail="Unauthorized request profile.")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT full_name, aadhaar_number, plaintext_password FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    
    response_data = [{"name": u[0], "aadhaar": u[1], "password": u[2]} for u in users]
    # FLAW: Leaking raw, unmasked PII and credentials directly to the log file (Violates DPDPA)
    logger.info(f"Authorized PII Export executed. Raw payload dumped to disk: {response_data}")
    return {"status": "success", "data": response_data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
