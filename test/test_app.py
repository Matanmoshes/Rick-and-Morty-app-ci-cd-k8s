import pytest
from app.rick_and_morty_rest_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_should_status_code_ok(client):
    response = client.get('/characters_data')
    assert response.status_code == 200