# ALVSIA AI UNCENSORED

Private owner-controlled Android AI client for the ALVSIA ecosystem.

## Goals

- Modern blue/white neon-metallic UI using the owner-provided ALVSIA AI UNCENSORED logo.
- Model catalog with user-selectable local and remote providers.
- ALVSIA panel integration boundary at https://alvsiapanel.unaux.com.
- No provider API secrets embedded in the APK.
- Device/license authorization remains server-side.
- Support for OpenAI-compatible gateways and Ollama-compatible local endpoints.
- Owner identity: @OriginalOnwerALV
- Telegram channel: https://t.me/ALVISIACHANEL

## Architecture

APK -> ALVSIA Panel authorization -> AI gateway/provider -> selected model.

The APK contains no model weights and no master secrets. Model metadata can be refreshed from an owner-controlled catalog endpoint.

## License

The ALVSIA application code is owner-controlled. Third-party model weights, runtimes and SDKs remain subject to their own licenses.
