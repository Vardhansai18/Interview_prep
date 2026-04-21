import pytest
import logging


LOG = logging.getLogger(__name__)


# Function-level tests (optional)
def test_file_1_tc1(module_fixture, session_fixture, function_fixture, class_fixture):
    LOG.info("test_file_1_tc1\n")
    pass


def test_file_1_tc2(module_fixture, session_fixture, function_fixture, class_fixture):
    LOG.info("test_file_1_tc2\n")
    pass


# # Class-level tests
# class Test_file_1:

#     def test_class_file_1_tc1(self, module_fixture, session_fixture, function_fixture, class_fixture):
#         pass

#     def test_class_file_1_tc2(self, module_fixture, session_fixture, function_fixture, class_fixture):
#         pass