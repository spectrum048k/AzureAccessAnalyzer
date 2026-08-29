import datetime

from azure.azure_api import AzureAPI
from azure.azure_activity_logs import AzureActivityLogs


def test_is_valid_guid_true():
    az_api = AzureAPI()
    assert az_api.is_valid_guid("12345678-1234-5678-1234-567812345678") == True


def test_is_valid_guid_false():
    az_api = AzureAPI()
    assert az_api.is_valid_guid("12345678-1234-5678-1234-56781234567") == False


def test_is_valid_guid_none():
    az_api = AzureAPI()
    assert az_api.is_valid_guid(None) == False


def test_get_activity_log_omits_none_select(monkeypatch):
    captured = {}

    class FakeResponse:
        status_code = 200
        text = "{}"

        def json(self):
            return {"value": []}

    def fake_http_get(self, url):
        captured["url"] = url
        return FakeResponse()

    monkeypatch.setattr(AzureAPI, "http_get", fake_http_get)
    monkeypatch.setattr(AzureAPI, "check_response", lambda self, response: response.json())

    start_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)
    end_date = datetime.datetime.now(datetime.timezone.utc)

    logs = AzureActivityLogs()
    result = logs.get_activity_log(
        "12345678-1234-5678-1234-567812345678",
        start_date,
        end_date,
        userName="test-user@example.com",
    )

    assert result == {"value": []}
    assert "&None" not in captured["url"]
    assert "api-version=2017-03-01-preview" in captured["url"]
