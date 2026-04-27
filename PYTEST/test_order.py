import pytest

@pytest.mark.order(2)
def test_second():
    print("Second")
    assert True

@pytest.mark.order(1)
def test_first():
    print("First")
    assert True

@pytest.mark.order(3)
def test_third():
    print("Third")
    assert True