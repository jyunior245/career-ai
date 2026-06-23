import pytest


@pytest.fixture
def mock_env(monkeypatch) -> None:
    """Mock environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test_career_ai.db")
    monkeypatch.setenv("DEBUG", "False")
