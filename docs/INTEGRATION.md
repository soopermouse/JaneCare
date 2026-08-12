# JaneOS Integration

JaneOS should register JaneCare using `janecare.app.yaml` and use:

- `GET /api/janeos/manifest`
- `GET /api/janeos/health`
- `GET /api/janeos/state`
- `GET /api/janeos/metrics`
- `GET /api/janeos/events`
- `POST /api/janeos/commands`

The command surface is allow-listed. JaneCare remains responsible for enforcing domain boundaries even if a caller has JaneOS-level privileges.
