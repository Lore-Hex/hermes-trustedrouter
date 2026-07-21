# hermes-trustedrouter

A standalone [Hermes Agent](https://github.com/NousResearch/hermes-agent) model
provider plugin for [TrustedRouter](https://trustedrouter.com), an
OpenAI/OpenRouter-compatible LLM router.

Per the Hermes plugin policy, third-party providers ship as standalone plugins
rather than in the Hermes core tree. This repo packages TrustedRouter as a
drop-in user plugin.

## Install

Drop the plugin directory into your `$HERMES_HOME` (defaults to `~/.hermes`):

```bash
git clone https://github.com/Lore-Hex/hermes-trustedrouter
mkdir -p "${HERMES_HOME:-$HOME/.hermes}/plugins/model-providers"
cp -r hermes-trustedrouter/plugins/model-providers/trustedrouter \
  "${HERMES_HOME:-$HOME/.hermes}/plugins/model-providers/"
```

Or symlink it so `git pull` keeps it current:

```bash
ln -s "$(pwd)/hermes-trustedrouter/plugins/model-providers/trustedrouter" \
  "${HERMES_HOME:-$HOME/.hermes}/plugins/model-providers/trustedrouter"
```

Hermes discovers user plugins under
`$HERMES_HOME/plugins/model-providers/<name>/` lazily on first
`get_provider_profile()` / `list_providers()` call — no repo edits, no restart
for subsequent sessions.

## Use

```bash
export TRUSTEDROUTER_API_KEY=***
hermes --provider trustedrouter --model trustedrouter/auto
```

Aliases: `tr`, `trusted-router`, `trustedrouter.com`, `quillrouter`,
`quill-router`. Optional `TRUSTEDROUTER_BASE_URL` overrides the endpoint.

## What it declares

- `base_url` `https://api.trustedrouter.com/v1`, `auth_type` `api_key`
- reasoning payloads passed through in OpenRouter/OpenAI-compatible form
- live model catalog from `{base_url}/models`, cached per process;
  `trustedrouter/auto` as the offline fallback

## Test

```bash
pip install pytest
pytest
```

The tests stub the Hermes `providers` module, so they run without a Hermes
install.

## License

MIT
