"""Unit tests for the TrustedRouter Hermes provider plugin (no Hermes install needed)."""


def test_registers_one_profile(load_plugin):
    profile, _ = load_plugin
    assert profile.name == "trustedrouter"


def test_endpoint_and_auth(load_plugin):
    profile, _ = load_plugin
    assert profile.base_url == "https://api.trustedrouter.com/v1"
    assert profile.env_vars == ("TRUSTEDROUTER_API_KEY", "TRUSTEDROUTER_BASE_URL")
    assert profile.signup_url == "https://trustedrouter.com/"


def test_aliases_present(load_plugin):
    profile, _ = load_plugin
    for alias in ("tr", "trusted-router", "quill-router"):
        assert alias in profile.aliases


def test_offline_fallback_model(load_plugin):
    profile, _ = load_plugin
    assert profile.fallback_models == ("trustedrouter/auto",)


def test_reasoning_extras_passthrough(load_plugin):
    profile, _ = load_plugin
    # supports_reasoning=False → no reasoning payload
    assert profile.build_api_kwargs_extras(supports_reasoning=False) == ({}, {})
    # explicit config is passed through as an OpenRouter/OpenAI-compatible reasoning block
    extra_body, top = profile.build_api_kwargs_extras(
        supports_reasoning=True, reasoning_config={"effort": "high"}
    )
    assert extra_body == {"reasoning": {"effort": "high"}}
    assert top == {}
    # default when enabled with no config
    extra_body, _ = profile.build_api_kwargs_extras(supports_reasoning=True)
    assert extra_body == {"reasoning": {"enabled": True, "effort": "medium"}}


def test_fetch_models_swallows_errors(load_plugin, monkeypatch):
    """A catalog fetch failure returns None rather than raising into discovery."""
    profile, _ = load_plugin
    base = profile.__class__.__mro__[1]  # the stub ProviderProfile

    def boom(self, *, api_key=None, timeout=8.0):
        raise RuntimeError("network down")

    monkeypatch.setattr(base, "fetch_models", boom)
    assert profile.fetch_models(api_key=None) is None
