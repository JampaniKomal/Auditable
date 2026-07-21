# Auditable

Auditable is an open-source Governance, Risk, and Compliance training lab for local security and compliance practice. It provides intentionally vulnerable enterprise environments that can be deployed with Docker Compose and audited with tools such as TraceState.

The goal of the project is practical training: reproduce realistic configuration drift, identify policy violations, and validate automated or manual audit workflows against known-bad systems.

## What’s Included

- Scenario 01: Fintech Startup
- Scenario 02: Legacy Enterprise
- Scenario 03: Healthcare Data Broker

Each scenario is isolated and documented with its own deployment instructions and audit guide.

## Repository Standards

- Open-source friendly structure with a clear root README, scenario-level documentation, and a top-level license.
- Repeatable local deployment through Docker Compose.
- Explicit separation between target environments and future audit tooling.
- Generated data and runtime artifacts are excluded from version control.

## Quick Start

1. Clone the repository.
2. Change into a scenario directory, for example `scenarios/01-fintech-startup`.
3. Start the target with `docker compose up -d`.
4. Review that scenario’s `audit_guide.md` for the intended findings.
5. Stop the stack with `docker compose down -v` when finished.

## Scenario Overview

| Scenario | Focus | Primary Services | Ports |
| --- | --- | --- | --- |
| 01-Fintech-Startup | DPDPA 2026, ISO 27001 | FastAPI, PostgreSQL, Nginx, simulator | 8000, 8080 |
| 02-Legacy-Enterprise | SEBI CSCRF, cryptographic hygiene | Node.js, MySQL, Nginx, simulator | 3000, 8081, 8443 |
| 03-Healthcare-Data-Broker | HIPAA, CERT-In | FastAPI, Elasticsearch, Logstash, Nginx, simulator | 5000, 8082, 9200 |

## Project Structure

- `scenarios/01-fintech-startup` - Python and PostgreSQL microservice lab
- `scenarios/02-legacy-enterprise` - Legacy Node.js and MySQL portal
- `scenarios/03-healthcare-data-broker` - Medical telemetry broker with ELK pipeline

## Open Source Notes

- License: MIT
- Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md)
- Security disclosures: see [SECURITY.md](SECURITY.md)

## Responsible Use

These environments are intentionally insecure and are intended for local training, research, and demonstration only. Do not deploy them on internet-facing systems.