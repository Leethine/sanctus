import os, sys

sys.path.append('..')

from sanctus.load_config import LoadConfig
from sanctus.local_mode.command import CommandLine

banner = """
========================================
  Running Sanctus Web Terminal
  DATA_DIR is set to "/mnt/sanctus_db"
========================================
"""

if __name__ == "__main__":
  db_dir = "/mnt/sanctus_db"
  
  while True:
    print(banner)
    try:
      cmd = CommandLine(db_dir)
      cmd.run()
    except:
      print("==== Exception occurred during execution... ====")
      print("==== Starting new session... ====")
