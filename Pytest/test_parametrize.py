import pytest

@pytest.mark.parametrize("username,password", [
    ("admin", "admin123"),
    ("user1", "pass1"),
    ("user2", "wrongpass")
])
def test_login(username, password):
    print(f"Testing with {username} / {password}")
    assert username != "" and password != ""