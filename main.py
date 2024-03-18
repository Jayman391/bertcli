import argparse

from src.bertcli._bertcli import BERTCLI

def main():
    
  parser = argparse.ArgumentParser(description="BERTopic CLI")

  parser.add_argument(
      "--data", type=str, required=False, help="Path to the global data file"
  )
  parser.add_argument(
      "--config", type=str, required=False, help="Path to the global config file"
  )

  args = parser.parse_args()

  cli = BERTCLI(global_data_path=args.data, global_config_path=args.config)

if __name__ == "__main__":
    
  main()
