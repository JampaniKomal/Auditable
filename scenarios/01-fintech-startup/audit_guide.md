# Audit Walkthrough: Scenario 01 (Fintech Startup)

This environment simulates a production financial infrastructure containing critical design layer errors that violate standard enterprise compliance structures.

## Technical Evidentiary Findings

### 1. Cryptographic Safeguards & Privacy (DPDPA 2026 / ISO 27001 Annex A.10)
*   **The Finding:** Navigate to the local `./logs/app_audit.log` file after hitting the endpoint. Notice that the application dumps unhashed, unmasked Aadhaar numbers and raw authentication strings directly into cleartext storage files.
*   **The Impact:** Direct non-compliance with the protection architectures mandated for processing sensitive personal data.

### 2. Access Control Manipulation (ISO 27001 Control A.9)
*   **The Finding:** Inspect `src/api.py`. The authorization verification parameters depend on a static string value checking rule (`MASTER_BACKDOOR_KEY_2026`).
*   **The Impact:** The usage of static administrative credential tokens bypasses core identity verification layers and leaves the perimeter vulnerable to credential leakage.

### 3. Basic Container Hardening (CIS Benchmarks / Least Privilege)
*   **The Finding:** The configuration declaration utilizes `user: root` inside the runtime environment manifest.
*   **The Impact:** Any runtime compromise allowing arbitrary code execution instantly inherits root administrative space capabilities on the host node instance.

### 4. Client-Side Secret Exposure (OWASP Top 10 / ISO 27001)
*   **The Finding:** Open the dashboard at `http://localhost:8080`, inspect the page source, and locate the hardcoded `MASTER_BACKDOOR_KEY_2026` token inside the JavaScript fetch logic.
*   **The Impact:** Exposing authorization tokens in client-side code destroys the trust boundary and gives any user the ability to replay the administrative request.
