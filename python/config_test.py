from config import OLLAMA_MODEL, OLLAMA_TIMEOUT, OLLAMA_URL


def test_default_ollama_configuration():
    assert OLLAMA_MODEL == "qwen3:1.7b"
    assert OLLAMA_URL == "http://localhost:11434/api/generate"
    assert OLLAMA_TIMEOUT == 60


def test_ollama_model_can_be_overridden(monkeypatch):
    monkeypatch.setenv("OLLAMA_MODEL", "qwen3:4b-q4_K_M")

    import importlib
    import config

    importlib.reload(config)

    assert config.OLLAMA_MODEL == "qwen3:4b-q4_K_M"


def test_ollama_timeout_can_be_overridden(monkeypatch):
    monkeypatch.setenv("OLLAMA_TIMEOUT", "120")

    import importlib
    import config

    importlib.reload(config)

    assert config.OLLAMA_TIMEOUT == 120
    assert isinstance(config.OLLAMA_TIMEOUT, int)
    

def test_ollama_url_can_be_overridden(monkeypatch):
    monkeypatch.setenv(
        "OLLAMA_URL",
        "http://example.com/api/generate",
    )

    import importlib
    import config

    importlib.reload(config)

    assert config.OLLAMA_URL == "http://example.com/api/generate"