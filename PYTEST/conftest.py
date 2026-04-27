import pytest
import logging

LOG = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def session_fixture():
    LOG.info("fixture: session_fixture - setup")
    yield
    LOG.info("fixture: session_fixture - teardown")


@pytest.fixture(scope='module')
def module_fixture():
    LOG.info("fixture: module_fixture - setup")
    yield
    LOG.info("fixture: module_fixture - teardown")


@pytest.fixture(scope='class')
def class_fixture():
    LOG.info("fixture: class_fixture - setup")
    yield
    LOG.info("fixture: class_fixture - teardown")


@pytest.fixture(scope='function')
def function_fixture():
    LOG.info("fixture: function_fixture - setup")
    yield
    LOG.info("fixture: function_fixture - teardown")