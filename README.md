# Auditable: Vulnerable-by-Design Enterprise Environments

**Auditable** is an open-source Governance, Risk, and Compliance (GRC) training ground. It provides a collection of intentionally misconfigured corporate architectures designed to fail modern regulatory frameworks like ISO 27001, India's DPDPA 2026, and SEBI CSCRF.

This monorepo allows security researchers, compliance auditors, and developers to deploy fully functional, vulnerable corporate networks locally via Docker Compose to practice manual auditing or test automated GRC scanning tools (like TraceState).

## Current Scenarios
*   **01-Fintech-Startup:** A Python/PostgreSQL microservice environment containing severe data-at-rest vulnerabilities, hardcoded secrets, and DPDPA privacy violations.

## How to Use
1. Navigate to a scenario directory (e.g., `cd scenarios/01-fintech-startup`).
2. Boot the vulnerable infrastructure: `docker compose up -d`
3. Use the provided `audit_guide.md` in each folder to learn how to manually uncover the compliance failures.
4. Tear down the environment when finished: `docker compose down -v`

**Warning:** These environments are highly insecure by design. Do not deploy them on internet-facing production servers.