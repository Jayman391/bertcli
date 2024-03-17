from bertcli.menus._menu import Menu

class ScoringMenu(Menu):
  def __init__(self):
    is_root = False
    is_leaf = True
    options = [
      'silhouette_score',
      'calinski_harabasz_score',
      'davies_bouldin_score',
      'composite (all)'
    ]

    super().__init__(options, is_leaf, is_root)
