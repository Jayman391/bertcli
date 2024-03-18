import argparse

from src._bertcli import BERTCLI

def main():
    
  parser = argparse.ArgumentParser(description="BERTopic CLI")

  parser.add_argument(
      "--data", type=str, required=False, help="Path to the global data file"
  )
  parser.add_argument(
      "--tmconfig", type=str, required=False, help="Path to the global topic model config file"
  )
  parser.add_argument(
      "--optconfig", type=str, required=False, help="Path to the global optimization config file"
  )
  
  args = parser.parse_args()

  cli = BERTCLI(global_data_path=args.data, global_config_path=args.tmconfig, global_optmization_path=args.optconfig)

if __name__ == "__main__":
    
  main()
