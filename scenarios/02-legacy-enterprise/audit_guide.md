# Audit Walkthrough: Scenario 02 (Legacy Enterprise)

This environment simulates a legacy financial portal with weak cryptographic posture, static secrets, and unmasked audit trails.

## Technical Evidentiary Findings

### 1. Deprecated TLS Configuration (SEBI CSCRF / Cryptographic Hygiene)
*   **The Finding:** Inspect `nginx/default.conf` and note that the HTTPS server explicitly enables `TLSv1` and `TLSv1.1` alongside weak cipher preferences.
*   **The Impact:** Legacy protocol negotiation exposes the portal to downgraded transport security and violates modern hardening expectations for regulated financial systems.

### 2. Outdated Logging Dependency (SBOM / Supply Chain Risk)
*   **The Finding:** Open `src/package.json` and review the intentionally pinned `winston@2.4.5` logging library.
*   **The Impact:** The application manifest embeds a stale dependency profile, making the build difficult to attest and exposing the stack to known library-level risk.

### 3. Hardcoded Client-Side Secret (Access Control Failure)
*   **The Finding:** View the page source in the browser and locate the static `LEGACY_MASTER_OVERRIDE_2026` token inside the dashboard JavaScript.
*   **The Impact:** Any user can replay the request and bypass the intended access control boundary.

### 4. Plaintext Audit Logging and Unencrypted Data at Rest (ISO 27001 / Data Protection)
*   **The Finding:** Trigger the ledger export and inspect `./logs/legacy_audit.log`. The server records raw financial identifiers and temporary passwords in cleartext, while MySQL persists the same records to an unencrypted bind-mounted volume.
*   **The Impact:** This creates a complete breach path from frontend token exposure to backend exfiltration and physical disk compromise.
