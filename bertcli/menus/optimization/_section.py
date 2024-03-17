from bertcli.menus._menu import Menu

class SectionMenu(Menu):
  def __init__(self):
    is_root = False
    is_leaf = True
    options = [
      "LLM",
      "Dimensionality Reduction",
      "Clustering"
    ]

    super().__init__(options, is_leaf, is_root)