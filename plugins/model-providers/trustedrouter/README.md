# TrustedRouter model provider for Hermes Agent

Routes `hermes` inference through [TrustedRouter](https://trustedrouter.com), an
OpenAI/OpenRouter-compatible LLM router.

## Setup

```bash
export TRUSTEDROUTER_API_KEY=***
# optional: override the endpoint
# export TRUSTEDROUTER_BASE_URL=https://api.trustedrouter.com/v1
hermes --provider trustedrouter --model trustedrouter/auto
```

`hermes model` lists the live catalog; `hermes doctor` health-checks the key and
the `/models` endpoint. See the repository README for install options.
