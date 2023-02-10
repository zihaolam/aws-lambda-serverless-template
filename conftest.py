from create_table import run
from utils.test_helpers import signup_mock_account, signup_mock_partner
import logging
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_mock_users(request):
    # prepare something ahead of all tests

    run()
    try:
        signup_mock_account()
    except Exception as e:
        logging.exception(e)

    try:
        signup_mock_partner()
    except Exception as e:
        logging.exception(e)

    # add cleanup functions
    # request.addfinalizer(finalizer_function)
