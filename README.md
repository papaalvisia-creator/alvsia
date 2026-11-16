# ALVSIA AI UNCENSORED

Owner-controlled Android AI client for the ALVSIA ecosystem.

## Goals

- Modern blue/white neon-metallic UI using the owner-provided ALVSIA AI UNCENSORED logo.
- User-selectable model catalog for local and remote providers.
- No provider API secrets embedded in the APK.
- Device and entitlement authorization is handled outside the client.
- Support for OpenAI-compatible gateways and Ollama-compatible local endpoints.
- Owner identity: @OriginalOnwerALV
- Telegram channel: https://t.me/ALVISIACHANEL

## Architecture

The Android client talks to a configurable AI gateway and selected model/provider. The APK contains no model weights and no provider master secrets. Model metadata may be refreshed from an owner-controlled catalog endpoint.

## Security boundaries

- Provider credentials remain outside the APK.
- Client binaries must not contain master signing keys, provider secrets or private authorization secrets.
- Local Ollama/OpenAI-compatible endpoints are user-configured.
- Authorization and entitlement decisions are not trusted solely to client-side state.

## Project status

This repository is the dedicated source for the separate **ALVSIA AI UNCENSORED** Android application. It is independent from **ALVSIA SMART TOOL**.

## License

The ALVSIA application code is owner-controlled. Third-party model weights, runtimes and SDKs remain subject to their own licenses.


## Release target

The release pipeline produces one debug build and one independently signed release APK. Public project documentation intentionally contains no panel endpoint or panel-source details.
