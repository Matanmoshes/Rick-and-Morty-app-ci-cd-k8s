import pytest
import requests
from rick_and_morty_rest_app.app import app

@pytest.fixture
def client():
    """Provide a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client

def test_healthcheck_returns_ok(client):
    """Verify that the healthcheck endpoint responds with status OK."""
    response = client.get('/healthcheck')
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['status'] == 'OK'

def test_characters_data_mocked_response(client, monkeypatch):
    """Mock the external API call and verify that /characters_data returns a 200 status and expected format."""

    class MockAPIResponse:
        status_code = 200
        def json(self):
            return {
                "info": {"next": None},
                "results": [
                    {
                        "name": "Morty Smith",
                        "location": {"name": "Earth (C-500A)"},
                        "image": "https://rickandmortyapi.com/api/character/avatar/2.jpeg"
                    }
                ]
            }

    def mock_requests_get(*args, **kwargs):
        return MockAPIResponse()

    # Monkeypatch the requests.get call to return the mock response
    monkeypatch.setattr(requests, "get", mock_requests_get)

    response = client.get('/characters_data')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['Name'] == "Morty Smith"
    assert "Earth" in data[0]['Location']
