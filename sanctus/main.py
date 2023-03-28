import os, sys

if __name__ == "__main__":
  sys.path.append('..')
  sys.path.append('.')

from sanctus.load_config import LoadConfig
from sanctus.local_mode.command import CommandLine as LMCommandLine

if __name__ == "__main__":
  home_dir = os.path.expanduser('~')
  print("[INFO] Home DIR: " + home_dir)
  cfg = LoadConfig(home_dir+"/.sanctus_config.json")
  db_dir = cfg.getDbDir()
  
  print("[INFO] DB DIR: " + db_dir)
  if cfg.getMode() == "local":
    cmd = LMCommandLine(db_dir)
    cmd.run()