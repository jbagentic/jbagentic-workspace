# Services

Acme's backend services. Each service owns its own README — read the service's
README first for its behavior and configuration.

- [billing/](billing/) — charges customers; handles payment-capture retries.
- [notify/](notify/) — sends user notifications (email, SMS, push).
- [payments/](payments/) — processes charges and refunds via the gateway.
- `auth/` — issues and refreshes tokens. No README; see its `AGENTS.md` for working rules.

## Event naming convention

This is the single source of truth for event names across **all** services;
individual service READMEs point here rather than restating it.

Every event a service emits is named `<service>.<entity>.<action>` — lowercase,
dot-separated, three parts. Examples: `billing.invoice.created`,
`notify.email.sent`.
