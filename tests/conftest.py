"""Stub the Hermes `providers` module so the plugin imports without a Hermes install.

Discovery in Hermes calls `register_provider(ProviderProfile(...))` at plugin
module load. We provide minimal stand-ins that faithfully capture the profile
kwargs and preserve subclassable, overridable hook methods, then load the real
plugin against them.
"""

import importlib.util
import sys
import types
from pathlib import Path

import pytest

PLUGIN_INIT = (
    Path(__file__).resolve().parent.parent
    / "plugins"
    / "model-providers"
    / "trustedrouter"
    / "__init__.py"
)


class _StubProfile:
    """Stand-in for providers.base.ProviderProfile — stores kwargs as attributes."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def fetch_models(self, *, api_key=None, timeout=8.0):
        # Base default in Hermes hits {base_url}/models; the stub returns None so
        # tests never make network calls.
        return None


@pytest.fixture
def load_plugin():
    """Import the plugin fresh against stub `providers` modules; return the registered profile."""
    registered = []

    providers_mod = types.ModuleType("providers")
    providers_mod.register_provider = registered.append  # type: ignore[attr-defined]
    base_mod = types.ModuleType("providers.base")
    base_mod.ProviderProfile = _StubProfile  # type: ignore[attr-defined]
    providers_mod.base = base_mod  # type: ignore[attr-defined]

    saved = {k: sys.modules.get(k) for k in ("providers", "providers.base")}
    sys.modules["providers"] = providers_mod
    sys.modules["providers.base"] = base_mod
    try:
        spec = importlib.util.spec_from_file_location("_tr_plugin_under_test", PLUGIN_INIT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert len(registered) == 1, f"expected one register_provider call, got {len(registered)}"
        yield registered[0], module
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
