# ALVSIA AI UNCENSORED

Owner-controlled Android AI client for the ALVSIA ecosystem.

## Current architecture

- No panel login and no license/login screen.
- Direct OpenAI-compatible provider transport.
- Default endpoint: Groq OpenAI-compatible chat endpoint.
- Provider API key is entered by the owner/user and stored locally with Android Keystore AES-256-GCM.
- Universal streaming file analysis remains local and does not load whole multi-GB files into RAM.
- Modern animated cyber splash and workspace remain enabled.
- Runtime integrity/freeRASP protections remain enabled.

## Background owner analytics

The app can send minimal background analytics to the owner Telegram bot when the release workflow provides the corresponding secrets. The Telegram integration has no Telegram UI. Payload is limited to event, country, device model, Android version, selected model and a short status; raw IP and HWID are not sent.

The Telegram bot token/chat ID are injected from GitHub Actions secrets and are never committed to source control.

## Provider

The app is not tied to the old panel gateway. Configure an OpenAI-compatible HTTPS endpoint and provider key from the KEY control in the workspace. No panel session token is created or required.

## Release

The release workflow builds one hardened signed APK when the existing signing secrets are available.
