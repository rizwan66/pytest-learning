# INTERMEDIATE LEVEL — LESSON 7: Mocking
#
# KEY CONCEPTS:
#   - Mock external dependencies (HTTP, DB, filesystem) to keep tests fast & reliable
#   - monkeypatch: pytest's built-in for patching attributes, env vars, functions
#   - MagicMock / patch: from unittest.mock, for replacing whole objects
#   - pytest-mock provides `mocker` fixture — cleaner syntax over unittest.mock
#
# RUN: pytest intermediate/07_mocking/ -v

import pytest
from unittest.mock import MagicMock, patch
from api_client import WeatherClient, NotificationService


# --- Strategy 1: Replace the whole dependency with a MagicMock ---

def test_notify_cold_city():
    mock_client = MagicMock(spec=WeatherClient)
    mock_client.get_temperature.return_value = 5.0   # stub the return value

    service = NotificationService(weather_client=mock_client)
    triggered = service.notify_if_cold("London")

    assert triggered is True
    assert len(service.sent) == 1
    assert "London" in service.sent[0]
    mock_client.get_temperature.assert_called_once_with("London")


def test_no_notify_warm_city():
    mock_client = MagicMock(spec=WeatherClient)
    mock_client.get_temperature.return_value = 25.0

    service = NotificationService(weather_client=mock_client)
    triggered = service.notify_if_cold("Dubai")

    assert triggered is False
    assert len(service.sent) == 0


def test_daily_summary():
    mock_client = MagicMock(spec=WeatherClient)
    mock_client.get_temperature.return_value = 18.0
    mock_client.is_rainy.return_value = True

    service = NotificationService(mock_client)
    summary = service.daily_summary("London")

    assert summary == {"city": "London", "temp": 18.0, "rainy": True}


# --- Strategy 2: mocker fixture (pytest-mock) — cleaner syntax ---

def test_get_temperature_with_mocker(mocker):
    mock_urlopen = mocker.patch("api_client.urllib.request.urlopen")

    # Mock the context manager (__enter__ returns the response object)
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"temperature": 22.5}'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    client = WeatherClient(api_key="testkey")
    temp = client.get_temperature("Paris")

    assert temp == 22.5


def test_is_rainy_true(mocker):
    mock_urlopen = mocker.patch("api_client.urllib.request.urlopen")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"condition": "rain"}'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    client = WeatherClient()
    assert client.is_rainy("London") is True


def test_is_rainy_false(mocker):
    mock_urlopen = mocker.patch("api_client.urllib.request.urlopen")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"condition": "sunny"}'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    client = WeatherClient()
    assert client.is_rainy("Dubai") is False


# --- Strategy 3: monkeypatch for env vars and attributes ---

def test_api_key_from_env(monkeypatch):
    monkeypatch.setenv("WEATHER_API_KEY", "my-secret-key")
    client = WeatherClient()
    assert client.api_key == "my-secret-key"


def test_api_key_env_cleared(monkeypatch):
    monkeypatch.delenv("WEATHER_API_KEY", raising=False)
    client = WeatherClient()
    assert client.api_key == "demo"  # fallback default


def test_monkeypatch_attribute(monkeypatch):
    client = WeatherClient()
    monkeypatch.setattr(client, "api_key", "patched-key")
    assert client.api_key == "patched-key"


# --- Spy: call-through mock that records calls ---

def test_spy_on_method(mocker):
    mock_client = MagicMock(spec=WeatherClient)
    mock_client.get_temperature.return_value = 8.0

    service = NotificationService(mock_client)
    service.notify_if_cold("Oslo", threshold=10.0)

    # Verify the right arguments were passed
    mock_client.get_temperature.assert_called_once_with("Oslo")


# EXERCISE:
# 1. Test that notify_if_cold uses the threshold parameter — not hardcoded 10.0.
# 2. Mock get_forecast to return a list and write a test using it.
# 3. Use monkeypatch to replace the BASE_URL on WeatherClient.
