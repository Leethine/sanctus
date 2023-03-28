import os, sys

if __name__ == "__main__":
  sys.path.append('..')
  sys.path.append('.')

from sanctus.load_config import LoadConfig
from sanctus.local_mode.command import CommandLine

if __name__ == "__main__":
  MAX_TRIAL = 99999
  db_dir = "/mnt/sanctus_db"

  print("[INFO] DB DIR: " + db_dir)
  for i in range(MAX_TRIAL):
    try:
      cmd = CommandLine(db_dir)
      cmd.run()
    except:
      print("[WARNING] Broken... Retry...")
      pass
