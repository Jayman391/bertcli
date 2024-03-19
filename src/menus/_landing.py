from src.menus._menu import Menu
from src.menus.topic._topic import TopicMenu
from util._session import Session

class Landing(Menu):
    def __init__(self, session:Session):
        is_root = True
        is_leaf = False
        options = [
            "Run a Topic Model",
            "Run an Optimization routine for a Topic Model (GPU reccomended)",
            "Run a Classification Model on a Topic Model",
            ]
        menus = [
            TopicMenu(session),
            None,
            None,
        ]
        if session.data is None:
            options.append("Load Global Data")
            menus.append(None)
        if session.config_topic_model is None:
            options.append("Load Global Topic Model Configuration")
            menus.append(None)
        if session.config_optimization is None:
            options.append("Load Global Optimization Configuration")
            menus.append(None)
        super().__init__(session, options, is_leaf, is_root)
        self._map_options_to_menus(options, menus)

