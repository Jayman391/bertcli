import pytest
from menus._landing import Landing
from util._session import Session
from src.menus.topic._topic import TopicMenu

session = Session("test_data/data.csv", "test_data/config.json", "test_data/config-opt.json")

def test_init_data():
    landing = Landing(session)
    
    # Check if the options and menus are initialized correctly
    assert landing.options == [
        "Run a Topic Model",
        "Run an Optimization routine for a Topic Model (GPU reccomended)",
        "Run a Classification Model on a Topic Model",
        "Exit"
    ]
    assert isinstance(list(landing.menus.values())[0], TopicMenu)
    with pytest.raises(SystemExit):
            landing.handle_choice(4)
    
    # Check if the is_root and is_leaf attributes are set correctly
    assert landing.is_root == True
    assert landing.is_leaf == False

def test_init_no_data():
    # Check if the options and menus are updated based on session data and configurations
    session.data = []
    session.config_topic_model = {}
    session.config_optimization = {}
    landing = Landing(session)
    assert landing.options == [
        "Run a Topic Model",
        "Run an Optimization routine for a Topic Model (GPU reccomended)",
        "Run a Classification Model on a Topic Model",
        "Load Global Data",
        "Load Global Topic Model Configuration",
        "Load Global Optimization Configuration",
        "Exit"
    ]
    assert type(list(landing.menus.values())[0]) == TopicMenu
    with pytest.raises(SystemExit):
                landing.handle_choice(7)