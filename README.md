# JaneCare

JaneCare is an AI-assisted social-care coordination and case-management application designed to be managed by Jane through JaneOS.

It provides four application surfaces:

- **JaneCare Core / Professional Dashboard** — case continuity, tasks, alerts, documents, appointments and human review.
- **Provider Network** — restricted provider access for referrals, status updates, information requests and service delivery.
- **Government Gateway** — jurisdiction adapters for reporting/validation with an explicit human-authorization boundary before consequential submission.
- **JaneOS Management Adapter** — a standard management contract so Jane can inspect state, monitor health, receive events, assign work and issue permitted commands.

## Important boundary

JaneCare may automate clerical work, preparation, matching, scheduling, follow-up, anomaly detection and reporting. Consequential decisions involving eligibility, safeguarding, coercive intervention, denial of assistance, benefit suspension, medical judgment, housing intervention or binding legal determinations remain under accountable human control.

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

Open:

- Dashboard: http://localhost:8090/
- API docs: http://localhost:8090/docs

For a Python-only local run:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8090
```

## JaneOS management contract

JaneOS interacts with JaneCare through `/api/janeos/*` endpoints. The application manifest is in `janecare.app.yaml`. The contract is intentionally generic so the same adapter shape can be reused by other external applications.

Copyright © 2026 Simona D. Thrussell, PhD / NXD Tech. All rights reserved.
