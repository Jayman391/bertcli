from src.menus._menu import Menu
from loading._dataloader import DataLoader

class ConfigMenu(Menu):
  def __init__(self, session):
    is_root = False
    is_leaf = True
    options = [
      "Input Data Path",
      "Input Topic Model Config Path",
      "Input Optimization Config Path",
    ]

    super().__init__(session, options, is_leaf, is_root)

    self.name = "Configuration"

    self.map_options_to_menus(options, [None, None, None])

 
  def handle_choice(self, choice: int):
      if choice == len(self.options):
          self.exit()
      elif choice == len(self.options) - 1:
          return self.back()
  
      loader = DataLoader()

      if choice == 1:
          prompt = input("Enter the path to the data file: ")
          if prompt.endswith(".csv") or prompt.endswith(".json"):
              self.session.set_data(loader._load_data(prompt))
              return self
          else:
            return self

      elif choice == 2:
          prompt = input("Enter the path to the topic model config file: ")
          if prompt.endswith(".json"):
              self.session.set_config_topic_model(loader._load_data(prompt))
              return self
          else:
            return self
      elif choice == 3:
          prompt = input("Enter the path to the optimization config file: ")
          if prompt.endswith(".json"):
            self.session.set_config_optimization(loader._load_data())
            return self
          else:
            return self
      else:
          return self.back()
