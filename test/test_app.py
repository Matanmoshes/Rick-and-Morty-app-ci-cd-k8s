import pytest
import requests
from app.rick_and_morty_rest_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_healthcheck(client):
    response = client.get('/healthcheck')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'OK'

def test_characters_data(client, monkeypatch):
    # Mock the requests.get call so we don't hit the actual external API.
    class MockResponse:
        status_code = 200
        def json(self):
            return {
                "info": {"next": None},
                "results": [
                    {
                        "name": "Rick Sanchez",
                        "location": {"name": "Earth (C-137)"},
                        "image": "https://rickandmortyapi.com/api/character/avatar/1.jpeg"
                    }
                ]
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    response = client.get('/characters_data')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['Name'] == "Rick Sanchez"
    assert "Earth" in data[0]['Location']
