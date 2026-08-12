# JaneCare Architecture

```text
Jane / JaneOS
    |
    | standard management contract
    v
JaneCare Management Adapter
    |
    +-- JaneCare Core / Professional Dashboard
    +-- Provider Network
    +-- Government Integration Gateway
    +-- Existing / future domain workers
```

## Management direction

JaneOS can inspect manifest, health, state, metrics and events, and may issue commands from JaneCare's explicit permitted-command set. Unknown or consequential commands are blocked at the application boundary.

## Government gateway

JaneCare uses a canonical internal report model. Jurisdiction adapters transform and validate that model. External transport is intentionally separated from report preparation. Production government adapters must be implemented and verified against the current official specification for the target jurisdiction and service domain.

## Provider access

The provider interface is a restricted operational surface. Production deployments must add real identity, tenant/provider scoping, RBAC/ABAC, audit retention, consent/legal-basis controls, encryption and data-minimization policies.
