# JaneCare authentication and authorization

JaneCare 0.2 adds five principal classes: professional/user, external provider, client, government and administrator. JaneOS uses a separate service identity and is not represented as a human account.

## Access boundaries

- Professional: assigned cases, professional dashboard, recommendations, permitted provider coordination, reporting preparation/validation.
- External provider: referrals assigned to that provider organization only.
- Client: own case summary and services only. No professional notes or other cases.
- Government: reporting gateway only, restricted to configured jurisdictions. No unrestricted case browsing.
- Administrator: operational administrative access across JaneCare.
- JaneOS: service-key authenticated management interface with the adapter's command allow-list.

The included account store and HMAC token implementation are self-contained development scaffolding. Production deployments should replace the demo identity store with a database or external identity provider, require TLS, rotate secrets, use strong password hashing/SSO/MFA where appropriate, and retain the route-level authorization and audit boundaries.

## Required secrets

Set `JANECARE_AUTH_SECRET` and `JANEOS_SERVICE_KEY` to long random secrets. The defaults deliberately contain `change-me-before-production` and must never be used outside local testing.
