import os, sys

if __name__ == "__main__":
  sys.path.append('..')
  sys.path.append('.')

from sanctus.load_config import LoadConfig
from sanctus.local_mode.command import CommandLine

if __name__ == "__main__":
  db_dir = "/home/lizian/.sanctus_data"

  print("[INFO] DB DIR: " + db_dir)
  try:
    cmd = CommandLine(db_dir)
    cmd.run()
  except:
    print("[ERROR] Broken.")
    pass
