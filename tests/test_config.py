"""Tests for configuration management."""

import os
import pytest
from src.config import Settings, get_api_key


class TestConfig:
    """Test suite for configuration management."""

    def test_get_api_key_from_env(self, monkeypatch):
        """Test getting API key from environment."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key-123")
        api_key = get_api_key()
        assert api_key == "test-key-123"

    def test_get_api_key_missing(self, monkeypatch):
        """Test error when API key is missing."""
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

        with pytest.raises(ValueError, match="GOOGLE_API_KEY not found"):
            get_api_key()

    def test_settings_defaults(self, monkeypatch):
        """Test default settings values."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key")

        settings = Settings()

        assert settings.google_api_key == "test-key"
        assert settings.default_model == "gemini-2.5-flash"
        assert settings.default_store_name == "default-store"
        assert settings.max_file_size_mb == 100

    def test_settings_custom_values(self, monkeypatch):
        """Test custom settings values."""
        monkeypatch.setenv("GOOGLE_API_KEY", "custom-key")
        monkeypatch.setenv("DEFAULT_MODEL", "gemini-2.5-pro")
        monkeypatch.setenv("DEFAULT_STORE_NAME", "my-store")
        monkeypatch.setenv("MAX_FILE_SIZE_MB", "50")

        settings = Settings()

        assert settings.google_api_key == "custom-key"
        assert settings.default_model == "gemini-2.5-pro"
        assert settings.default_store_name == "my-store"
        assert settings.max_file_size_mb == 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
