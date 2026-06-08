import pytest


# Первая фикстура — даёт id
@pytest.fixture(params=[1, 2, 3])
def user_id(request):
    return request.param


# Вторая фикстура — даёт имя
@pytest.fixture(params=["Alice", "Bob", "Charlie"])
def user_name(request):
    return request.param


def greet_user(uid, name):
    return f"Hello, user {name} with id {uid}"


def test_greet_user(user_id, user_name):
    greeting = greet_user(user_id, user_name)