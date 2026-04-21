
import pytest 

@pytest.fixture
def suitesetupandclean():
    print("suite setup\n")
    yield
    print("suite clean up\n")


def test_case1(suitesetupandclean):
    print("exectution of the test case 1\n")