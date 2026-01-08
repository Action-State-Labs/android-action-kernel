import pytest
import os
from unittest.mock import patch
from llm_manager import LLMManager

def test_init_openai_provider():
    with patch.dict(os.environ, {
        "LLM_PROVIDER": "openai",
        "OPENAI_API_KEY": "test-key",
        "OPENAI_MODEL": "gpt-4o"
    }):
        manager = LLMManager()
        assert manager.provider == "openai"
        assert manager.model == "gpt-4o"

def test_init_anthropic_provider():
    with patch.dict(os.environ, {
        "LLM_PROVIDER": "anthropic",
        "ANTHROPIC_API_KEY": "test-key",
        "ANTHROPIC_MODEL": "claude-sonnet-4"
    }):
        manager = LLMManager()
        assert manager.provider == "anthropic"
        assert manager.model == "claude-sonnet-4"

def test_missing_provider_raises_error():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="LLM_PROVIDER"):
            LLMManager()

def test_missing_api_key_raises_error():
    with patch.dict(os.environ, {"LLM_PROVIDER": "openai"}, clear=True):
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            LLMManager()

def test_default_models():
    with patch.dict(os.environ, {
        "LLM_PROVIDER": "openai",
        "OPENAI_API_KEY": "test-key"
    }, clear=True):
        manager = LLMManager()
        assert manager.model == "gpt-4o"  # default
