import pytest
import requests

@pytest.mark.parametrize("breed", ["hound", "bulldog"])
def test_dog_ceo_random_image(breed):
    url = f"https://dog.ceo/api/breed/{breed}/images/random"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert 'https://' in response.json()['message']

def test_valid_sub_breeds():
    url = "https://dog.ceo/api/breed/hound/list"
    response = requests.get(url)
    assert response.status_code == 200
    sub_breeds = response.json()['message']
    print(sub_breeds)

@pytest.mark.parametrize("sub_breed", ["plott", "walker"])
def test_dog_ceo_sub_breeds(sub_breed):
    url = f"https://dog.ceo/api/breed/hound/{sub_breed}/images/random"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert 'https://' in response.json()['message']

@pytest.mark.parametrize("invalid_breed", ["xyz", "123"])
def test_dog_ceo_invalid_breed(invalid_breed):
    url = f"https://dog.ceo/api/breed/{invalid_breed}/images/random"
    response = requests.get(url)
    assert response.status_code == 404
