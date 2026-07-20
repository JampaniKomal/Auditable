# Audit Walkthrough: Fintech Startup

This environment simulates a rapidly scaling financial technology company. While the application functions, the underlying infrastructure violates critical data protection and security frameworks. 

As an auditor, your goal is to map the technical configurations to legal violations.

## 1. ISO 27001 Violation: Principle of Least Privilege
*   **The Flaw:** The `employee-portal` container in `docker-compose.yml` is explicitly set to execute as the `root` user (`user: root`).
*   **The Evidence:** Standard container security requires applications to run as non-root users. If an attacker breaches the FastAPI application, they instantly gain root-level access to the container filesystem.

## 2. Supply Chain / Configuration Violation: Hardcoded Secrets
*   **The Flaw:** The database connection strings are injected as plaintext environment variables (`DB_PASS=supersecretplaintext`) directly inside the Docker configuration.
*   **The Evidence:** Anyone with access to the source code repository or the Docker daemon can read the master database credentials.

## 3. DPDPA 2026 Violation: Unencrypted Data at Rest
*   **The Flaw:** The PostgreSQL database mounts to a local, unencrypted volume (`./data:/var/lib/postgresql/data`). 
*   **The Evidence:** The Digital Personal Data Protection Act (DPDPA) mandates strict safeguards for handling personal data. Because the host volume is not encrypted, a compromised host server allows an attacker to copy the raw database files and extract user data directly.

## 4. DPDPA & ISO 27001 Violation: Plaintext PII and Logging
*   **The Flaw:** The application (`api.py`) stores highly sensitive identifiers (Aadhaar numbers and passwords) in plaintext and logs them directly to standard output upon an API request.
*   **The Evidence:** DPDPA Section 8 requires reasonable security safeguards (like masking, tokenization, or encryption) for personal data. Storing and logging this data without cryptographic hashing makes the company legally liable for a massive fine in the event of a breach.
