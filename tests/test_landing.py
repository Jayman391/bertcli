import pytest
from menus._landing import Landing
from util._session import Session
from src.menus.topic._topic import TopicMenu
from src.menus._configmenu import ConfigMenu

session = Session(
    "test_data/data.csv", "test_data/config.json", "test_data/config-opt.json"
)


def test_init_data():
    landing = Landing(session)

    # Check if the options and menus are initialized correctly
    assert landing.options == [
        "Run a Topic Model",
        "Run a Classification Model",
        "Run an Optimization routine",
        "Load Global Configuration Files",
        "Exit",
    ]
    assert isinstance(list(landing.menus.values())[0], TopicMenu)
    assert list(landing.menus.values())[1] == None
    assert list(landing.menus.values())[2] == None
    assert isinstance(list(landing.menus.values())[3], ConfigMenu)

    # Check if the is_root and is_leaf attributes are set correctly
    assert landing.is_root == True
    assert landing.is_leaf == False
