import os
import time
import logging
import psycopg2
from fastapi import FastAPI, HTTPException
import uvicorn

# INTENTIONAL FLAW 4: Logging raw PII to standard output (Violates DPDPA data masking)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Delta Fintech Internal API")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "fintech_vault")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "supersecretplaintext")

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except psycopg2.Error as e:
            logger.error(f"Database connection failed. Retrying... {e}")
            retries -= 1
            time.sleep(2)
    raise Exception("Could not connect to database.")

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
            ('Priya Sharma', '987654321098', 'admin2026')
        """)
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Database initialized with unencrypted mock PII.")

@app.on_event("startup")
def startup_event():
    initialize_database()

@app.get("/api/users")
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT full_name, aadhaar_number, plaintext_password FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    
    response_data = [{"name": u[0], "aadhaar": u[1], "password": u[2]} for u in users]
    logger.info(f"API accessed. Leaking raw PII to logs: {response_data}")
    return {"status": "success", "data": response_data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
