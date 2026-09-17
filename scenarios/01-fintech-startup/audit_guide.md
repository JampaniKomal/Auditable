# Audit Walkthrough: Scenario 01 (Fintech Startup)

This environment simulates a production financial infrastructure containing critical design layer errors that violate standard enterprise compliance structures.

## Technical Evidentiary Findings

### 1. Cryptographic Safeguards & Privacy (DPDPA 2026 / ISO 27001 Annex A.10)
*   **The Finding:** Navigate to the local `./logs/app_audit.log` file after hitting the endpoint. Notice that the application dumps unhashed, unmasked Aadhaar numbers and raw authentication strings directly into cleartext storage files.
*   **Evidence:** `docker compose up -d --build`, then `curl -H "Authorization: Bearer MASTER_BACKDOOR_KEY_2026" http://localhost:8000/api/users`, then `tail logs/app_audit.log` — the response payload above is byte-for-byte reproduced in the log line.
*   **The Impact:** Direct non-compliance with the protection architectures mandated for processing sensitive personal data.
*   **Remediation:** Mask or tokenize PII (Aadhaar, passwords) before it reaches any logging call — log a hash or a redacted form, never the raw value. Store passwords hashed (e.g. bcrypt/argon2) so there is no raw value to leak in the first place. Apply log-level data classification review before any new log statement referencing a request/response body ships.

### 2. Access Control Manipulation (ISO 27001 Control A.9)
*   **The Finding:** Inspect `src/api.py`. The authorization verification parameters depend on a static string value checking rule (`MASTER_BACKDOOR_KEY_2026`).
*   **The Impact:** The usage of static administrative credential tokens bypasses core identity verification layers and leaves the perimeter vulnerable to credential leakage.
*   **Remediation:** Replace the static bearer token with per-user, short-lived credentials (OAuth2/JWT with expiry) issued by a real identity provider, and remove any single shared "master" credential entirely. If a service-to-service credential is genuinely needed, source it from a secrets manager and rotate it on a schedule, never hardcode it in source.

### 3. Basic Container Hardening (CIS Benchmarks / Least Privilege)
*   **The Finding:** The configuration declaration utilizes `user: root` inside the runtime environment manifest.
*   **The Impact:** Any runtime compromise allowing arbitrary code execution instantly inherits root administrative space capabilities on the host node instance.
*   **Remediation:** Run the container as a dedicated non-root user (`USER appuser` in a real Dockerfile, or `user: "1000:1000"` in compose), and drop any Linux capabilities the process doesn't explicitly need (`cap_drop: [ALL]`).

### 4. Client-Side Secret Exposure (OWASP Top 10 / ISO 27001)
*   **The Finding:** Open the dashboard at `http://localhost:8080`, inspect the page source, and locate the hardcoded `MASTER_BACKDOOR_KEY_2026` token inside the JavaScript fetch logic.
*   **The Impact:** Exposing authorization tokens in client-side code destroys the trust boundary and gives any user the ability to replay the administrative request.
*   **Remediation:** Never ship credentials in client-side code. Authenticate the browser session itself (e.g. a server-issued, httpOnly session cookie) and have the backend authorize per-user, rather than handing the browser a static bearer token it can replay.

## Visual Evidence

![Delta Fintech dashboard after clicking "Load Employee PII", showing three employees' names, unmasked Aadhaar numbers, and plaintext passwords in a table](docs/dashboard_screenshot.png)
