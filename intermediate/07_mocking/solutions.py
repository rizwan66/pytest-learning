# SOLUTIONS — Lesson 07: Mocking

from unittest.mock import MagicMock
import pytest
from api_client import WeatherClient, NotificationService


def test_notify_respects_custom_threshold():
    mock = MagicMock(spec=WeatherClient)
    mock.get_temperature.return_value = 12.0

    service = NotificationService(mock)
    # With default threshold 10: 12 > 10 → no alert
    assert service.notify_if_cold("Cairo", threshold=10.0) is False
    # With threshold 15: 12 < 15 → alert fires
    assert service.notify_if_cold("Cairo", threshold=15.0) is True


def test_get_forecast(mocker):
    mock_urlopen = mocker.patch("api_client.urllib.request.urlopen")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"forecast": ["sunny", "cloudy", "rain"]}'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    client = WeatherClient()
    forecast = client.get_forecast("London", days=3)
    assert forecast == ["sunny", "cloudy", "rain"]


def test_monkeypatch_base_url(monkeypatch):
    monkeypatch.setattr(WeatherClient, "BASE_URL", "https://test-api.example.com")
    client = WeatherClient()
    assert client.BASE_URL == "https://test-api.example.com"
