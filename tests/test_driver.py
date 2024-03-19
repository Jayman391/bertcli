from drivers._driver import Driver
from util._session import Session
from menus._menu import Menu


def test_initialize_session():
    driver = Driver()
    session = driver.initialize_session(
        data_path="tests/test_data/data.csv",
        config_path="tests/test_data/config.json",
        optimization_path=None,)
    assert session is not None

def test_log():
    driver = Driver()
    driver.initialize_session()
    assert driver.log(type="info", message="This is an info message") == {"info": "This is an info message"}
    assert "info" in driver.session.logs.keys()
    assert driver.session.logs["info"] == ["This is an info message"]

def test_run_menu():
    driver = Driver()
    menu = Menu(options=["Option 1", "Option 2"], is_leaf=True, is_root=True)
    # choose option 1
    assert driver.run_menu(menu) == "Option 1"

def test_run_model():
    driver = Driver()
    assert driver.run_model() is None