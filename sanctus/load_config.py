import os, json
from sanctus.constants import CONFIG_NON_VALID_ERR

class LoadConfig:
  def __init__(self, path: str) -> None:
    self.__CONFIG_FILE_PATH = ""
    self.__MODE = ""
    self.__DB_DIR = ""
    
    if os.path.exists(path):
      self.__CONFIG_FILE_PATH = os.path.abspath(path)
    else:
      print("[ERROR] Cannot find config file!")
      exit(CONFIG_NON_VALID_ERR)
    
    if self.readConfig():
      print("[INFO] Loaded config file.")
    else:
      print("[ERROR] Failed to load config!")
      exit(CONFIG_NON_VALID_ERR)
  
  def readConfig(self) -> bool:
    try:
      with open(self.__CONFIG_FILE_PATH, "r") as jfile:
        jobj = json.load(jfile)
        self.__MODE = jobj["mode"]
        self.__DB_DIR = jobj["data-directory"]
      return True
    except:
      return False
  
  def getMode(self) -> str:
    return self.__MODE
  
  def getDbDir(self) -> str:
    return os.path.abspath(self.__DB_DIR)
  