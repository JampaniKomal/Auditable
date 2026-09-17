# Auditable

Auditable is an open-source Governance, Risk, and Compliance training lab for local security and compliance practice. It provides intentionally vulnerable enterprise environments that can be deployed with Docker Compose and audited manually or with any compliance testing tool.

The goal of the project is practical training: reproduce realistic configuration drift, identify policy violations, and validate audit workflows against known-bad systems. Every finding documented in this repository was independently reproduced end-to-end while building it — not just written down and assumed correct (see "How this was verified" below).

## What's Included

- Scenario 01: Fintech Startup
- Scenario 02: Legacy Enterprise
- Scenario 03: Healthcare Data Broker

Each scenario is isolated and documented with its own deployment instructions and audit guide.

## Quick Start

1. Clone the repository.
2. Change into a scenario directory, for example `scenarios/01-fintech-startup`.
3. Start the target with `docker compose up -d`.
4. Review that scenario's `audit_guide.md` for the intended findings, evidence commands, and remediation guidance.
5. Stop the stack with `docker compose down -v` when finished.

## Scenario Overview

| Scenario | Focus | Primary Services | Ports |
| --- | --- | --- | --- |
| 01-Fintech-Startup | DPDPA 2026, ISO 27001 | FastAPI, PostgreSQL, Nginx, simulator | 8000, 8080 |
| 02-Legacy-Enterprise | SEBI CSCRF, cryptographic hygiene | Node.js, MySQL, Nginx, simulator | 3000, 8081, 8443 |
| 03-Healthcare-Data-Broker | HIPAA, CERT-In | FastAPI, Elasticsearch, Logstash, Nginx, simulator | 5000, 8082, 9200 |

## Compliance Framework Coverage

A single finding is rarely mapped to only one framework in practice, so this table is a starting index into each scenario's `audit_guide.md`, not an exhaustive control catalog.

| Framework / Standard | Relevant Control Area | Where It's Demonstrated |
| --- | --- | --- |
| DPDPA 2026 (India) | Processing and storage of personal data (Aadhaar, PII) | Scenario 01, Finding 1 |
| ISO 27001 Annex A.9 | Access control | Scenario 01 Finding 2, Scenario 02 Finding 3, Scenario 03 Finding 3 |
| ISO 27001 Annex A.10 / A.8 | Cryptography, data protection | Scenario 01 Finding 1, Scenario 02 Finding 4, Scenario 03 Finding 4 |
| CIS Benchmarks / Least Privilege | Container and host hardening | Scenario 01 Finding 3, Scenario 03 Finding 1 |
| SEBI CSCRF | Cryptographic hygiene for regulated financial systems | Scenario 02 Finding 1 |
| SBOM / Supply Chain Risk | Dependency vulnerability management | Scenario 02 Finding 2 |
| CERT-In | Breach/incident reporting timelines | Scenario 03 Finding 2 |
| HIPAA | Protected health information handling | Scenario 03 Finding 4 |
| OWASP Top 10 | Client-side secret exposure, broken access control | Scenario 01 Finding 4, and the client-secret finding in every scenario |

## How This Was Verified

Every documented finding was actually reproduced, not just written down:

- Each scenario was brought up with `docker compose up -d --build` and driven through its full flow (load data, trigger the intentional flaw, inspect the resulting log/index) rather than just reading the source.
- The Docker-socket escape in Scenario 03 was demonstrated for real: from inside the broker container, the Docker Engine API was queried over the mounted socket and returned the full list of host containers.
- `npm audit` / `pip-audit` were run against every scenario's pinned dependencies. This caught two real, unintentional problems that were fixed as part of building this lab (not part of the intended lesson):
  - Scenario 02's audit guide originally cited an incorrect dependency (`winston@2.4.5`, which the actual `package.json` didn't even pin, and which would have crashed the app's real winston-3.x-only logging setup). Replaced with a real, current, verified CVE in the pinned `mysql2` driver.
  - Scenarios 01 and 03's `fastapi`/`uvicorn`/`starlette` pins had multiple known CVEs unrelated to the intended lesson content; bumped to current versions and re-verified every finding still reproduces identically.
- Scenario 02's "deprecated TLS" finding was checked with an actual TLS handshake attempt (`openssl s_client -tls1` from a client whose OpenSSL still implements TLS 1.0), which revealed the server's own OpenSSL build rejects the handshake despite the config requesting it — the audit guide documents this nuance explicitly instead of overclaiming live exploitability.

Only the intentional, documented flaws remain by design (see each scenario's audit guide) — everything else found along the way was fixed.

## Project Structure

- `scenarios/01-fintech-startup` - Python and PostgreSQL microservice lab
- `scenarios/02-legacy-enterprise` - Legacy Node.js and MySQL portal
- `scenarios/03-healthcare-data-broker` - Medical telemetry broker with ELK pipeline

## Open Source Notes

- License: MIT
- Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md)
- Community expectations: see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Security disclosures: see [SECURITY.md](SECURITY.md)

## Responsible Use

These environments are intentionally insecure and are intended for local training, research, and demonstration only. Do not deploy them on internet-facing systems.
