from drivers._driver import Driver
from util._session import Session


def test_initialize_session():
    driver = Driver()
    session = driver.initialize_session(
        data_path="tests/test_data/data.csv",
        config_path="tests/test_data/config.json",
        optimization_path=None,)
    assert session is not None
    assert driver.session is not None

def test_log():
    driver = Driver()
    driver.initialize_session()
    assert driver.log(type="info", message="This is an info message") == {"info": "This is an info message"}
    assert "info" in driver.session.logs.keys()
    assert driver.session.logs["info"] == ["This is an info message"]


def test_run_menu():
    driver = Driver()
    assert driver.run_menu() is None


def test_build_model():
    driver = Driver()
    assert driver.build_model() is None


def test_run_model():
    driver = Driver()
    assert driver.run_model() is None