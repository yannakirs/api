import pytest
import requests

def test_mailru_status_code():
    response = requests.get("https://mail.ru/")
    assert response.status_code == 200

def test_google_status_code():
    response = requests.get("https://google.com/")
    assert response.status_code == 200

def test_nonexistent_url_status_code():
    response = requests.get("https://nonexistenturl123456789.com/")
    assert response.status_code == 404

@pytest.mark.parametrize("url, expected_status_code", [
    ("https://mail.ru/", 200),
    ("https://google.com/", 200),
    ("https://httpbin.org/status/404", 404),
    ("https://example.com/", 200),
    ("https://httpbin.org/status/500", 500),
])
def test_url_status_code(url, expected_status_code):
    response = requests.get(url)
    assert response.status_code == expected_status_code
