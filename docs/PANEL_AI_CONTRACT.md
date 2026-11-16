# Panel AI Contract

The Android client is deliberately separated from the live panel implementation.

Current base URL:
https://alvsiapanel.unaux.com

Required future server contract:
- authenticated session exchange
- model catalog endpoint
- model entitlement check
- chat completion endpoint
- usage/rate-limit response
- security event reporting

The client currently targets:
POST /api/ai/chat

This endpoint is an adapter contract and must be matched to the real panel routes before production release. No live panel files are changed by this repository.
