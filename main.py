import argparse

import sys
import os
# Get the current working directory
cwd = os.getcwd()
# Add the src directory to sys.path
sys.path.append(os.path.join(cwd, 'src'))

from _nllpcli import NLLPCLI

def main():
    
  parser = argparse.ArgumentParser(description="BERTopic CLI")

  parser.add_argument(
      "data", type=str, nargs="?", help="Path to the global data file"
  )
  parser.add_argument(
      "tmconfig", type=str, nargs="?", help="Path to the global topic model config file"
  )
  parser.add_argument(
      "optconfig", type=str, nargs="?", help="Path to the global optimization config file"
  )
  
  args = parser.parse_args()

  cli = NLLPCLI(global_data_path=args.data, global_config_path=args.tmconfig, global_optmization_path=args.optconfig)

if __name__ == "__main__":
    
  main()
