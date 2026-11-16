# ALVSIA AI Provider Contract

The Android client is deliberately separated from provider implementations.

Supported integration boundaries:
- OpenAI-compatible gateways
- Ollama-compatible local endpoints
- configurable model/provider selection
- authenticated provider sessions where required
- model catalog and entitlement metadata
- usage/rate-limit responses
- security event reporting

The client must never embed provider master secrets or private authorization credentials.
