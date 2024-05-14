import pytest
import requests
from github_exporter.github_copilot_exporter import fetch_enterprise_usage, fetch_org_billing

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise requests.HTTPError()

@pytest.fixture
def mock_responses(monkeypatch):
    def mock_get(*args, **kwargs):
        if 'usage' in args[0]:
            return MockResponse([{"language": "python", "editor": "vscode", "metric": 1234}], 200)
        elif 'billing' in args[0]:
            return MockResponse({"billing": 5678}, 200)

    monkeypatch.setattr(requests, "get", mock_get)

def test_fetch_enterprise_usage(mock_responses):
    usage = fetch_enterprise_usage('test_enterprise', 'test_org', 'test_token')
    assert usage is not None
    assert usage[0]["metric"] == 1234

def test_fetch_org_billing(mock_responses):
    billing = fetch_org_billing('test_enterprise', 'test_org', 'test_token')
    assert billing is not None
    assert billing["billing"] == 5678
