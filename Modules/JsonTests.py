import pytest
import requests
import allure

def test_jsonplaceholder_get_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    with allure.step("Requesting all posts"):
        response = requests.get(url)
    assert response.status_code == 200

def test_jsonplaceholder_get_post_by_id():
    post_id = 1
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    with allure.step(f"Requesting post with ID {post_id}"):
        response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['id'] == post_id

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_jsonplaceholder_get_posts_by_user(user_id):
    url = f"https://jsonplaceholder.typicode.com/posts?userId={user_id}"
    with allure.step(f"Requesting posts for user ID {user_id}"):
        response = requests.get(url)
    assert response.status_code == 200
    assert all(post['userId'] == user_id for post in response.json())

@pytest.mark.parametrize("post_id", [1, 3, 5])
def test_jsonplaceholder_get_comments_for_post(post_id):
    url = f"https://jsonplaceholder.typicode.com/comments?postId={post_id}"
    with allure.step(f"Requesting comments for post ID {post_id}"):
        response = requests.get(url)
    assert response.status_code == 200
    assert all(comment['postId'] == post_id for comment in response.json())

def test_jsonplaceholder_create_post():
    url = "https://jsonplaceholder.typicode.com/posts"
    data = {
        "title": "Test Title",
        "body": "Test Body",
        "userId": 1
    }
    with allure.step("Creating a new post"):
        response = requests.post(url, json=data)
    assert response.status_code == 201
    assert response.json()['id'] is not None
