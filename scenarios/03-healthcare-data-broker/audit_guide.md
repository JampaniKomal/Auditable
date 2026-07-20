# Audit Walkthrough: Scenario 03 (Healthcare Data Broker)

This environment simulates a medical telemetry broker with weak incident response design and dangerous container exposure.

## Technical Evidentiary Findings

### 1. Exposed Docker Socket (Container Escape Risk)
*   **The Finding:** Inspect `docker-compose.yml` and note that the public-facing broker service mounts `/var/run/docker.sock` into the container.
*   **The Impact:** Any compromise of the broker service can be escalated into host-level container control, violating basic isolation expectations.

### 2. Disconnected Webhooks (CERT-In / Incident Response)
*   **The Finding:** The dashboard and API both describe breach events as queued locally while the external webhook target remains unreachable.
*   **The Impact:** A real breach could fail to trigger mandatory incident reporting within the required timeline, creating a compliance blind spot.

### 3. Hardcoded Client Secret (Access Control Failure)
*   **The Finding:** Open the dashboard source and locate the static `CERTIN_MASTER_BYPASS_2026` token in browser JavaScript.
*   **The Impact:** The portal exposes its own administrative bypass key to any user who can view page source.

### 4. Cleartext Medical Telemetry in the ELK Pipeline
*   **The Finding:** The broker logs raw patient identifiers and telemetry events, and Logstash forwards them into Elasticsearch without masking.
*   **The Impact:** Sensitive medical data becomes searchable in plaintext across the audit pipeline, defeating privacy controls.
