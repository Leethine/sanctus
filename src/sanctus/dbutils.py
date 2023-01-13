import os, sys, io, shutil
import string, json
import constants

class File_IO():
  def __init__(self) -> None:
    pass

  def readJsonFileAsDict(self, fpath: str) -> dict:
    try:
      return json.load(fpath)
    except ValueError as e:
      print("Error reading {}: {}".format(fpath, e))
      return None
  
  def readJsonFileAsStr(self, fpath: str) -> str:
    return json.dumps(self.getJsonFileAsDict(fpath))
  
  def writeJsonFile(self, jsonobj: dict, fpath: str) -> None:
    try:
      json.dump(jsonobj, fpath)
    except ValueError as e:
      print("Error writing {}: {}".format(fpath, e))

  def writeJsonFile(self, jsonstr: str, fpath: str) -> None:
    self.writeJsonFile(json.loads(jsonstr), fpath)
  
  def readFileLines(self, fpath: str) -> list:
    try:
      with open(fpath, "r") as f:
        return f.readlines()
    except ValueError as e:
      print("Error reading {}: {}".format(fpath, e))
  
  def readFileAsStr(self, fpath: str) -> str:
    try:
      with open(fpath, "r") as f:
        return f.read()
    except ValueError as e:
      print("Error reading {}: {}".format(fpath, e))
  

  def fcopyReplace(self, from_path: str, to_path: str) -> str:
    try:
      if os.path.exists(to_path):
        os.remove(to_path)
      shutil.copy2(from_path, to_path)
    except RuntimeError as e:
      print("Error during fcopy: {}".format(e))
  
  def fcopyNoReplace(self, from_path: str, to_path: str) -> str:
    try:
      if os.path.exists(to_path):
        #print("fcopy: dst file exists, abort.")
        pass
      else:
        shutil.copy2(from_path, to_path)
    except RuntimeError as e:
      print("Error during fcopy: {}".format(e))
  
  def fmoveReplace(self, from_path: str, to_path: str) -> str:
    try:
      shutil.move(from_path, to_path, copy_function=shutil.copy2())
    except RuntimeError as e:
      print("Error during fmove: {}".format(e))

  def fmoveNoReplace(self, from_path: str, to_path: str) -> str:
    try:
      if os.path.exists(to_path):
        #print("fmove: dst file exists, abort.")
        pass
      else:
        shutil.move(from_path, to_path, copy_function=shutil.copy2())
    except RuntimeError as e:
      print("Error during fmove: {}".format(e))

class DB_Connect():
  def __init__(self, my_db_path: str) -> None:
    self.__dbpath = os.path.abspath(my_db_path)
    if not self.checkDBStructure(self.__dbpath):
      print("DB structure is invalid, please recreate DB, or check your path")
      exit(constants.DB_NON_VALID_ERR)

  def checkDBStructure(self, dbpath_to_check: str) -> bool:
    dbpath = os.path.abspath(dbpath_to_check)

    check = 1
    check *= os.path.exists(dbpath + "/_desc.json")
    
    # composer
    check *= os.path.exists(dbpath + "/composer/_desc.json")
    check *= os.path.exists(dbpath + "/composer/info/_desc.json")
    check *= os.path.exists(dbpath + "/composer/oeuvre/_desc.json")

    # metadata
    check *= os.path.exists(dbpath + "/metadata/_desc.json")
    check *= os.path.exists(dbpath + "/metadata/arrangement/_desc.json")
    check *= os.path.exists(dbpath + "/metadata/collection/_desc.json")
    check *= os.path.exists(dbpath + "/metadata/piece/_desc.json")
    check *= os.path.exists(dbpath + "/metadata/template/_desc.json")
    
    # score
    check *= os.path.exists(dbpath + "/score/_desc.json")
    check *= os.path.exists(dbpath + "/score/template/_desc.json")
    check *= os.path.exists(dbpath + "/score/file/_desc.json")
    file_dir = list(string.digits + string.ascii_lowercase)
    for dir in file_dir:
      check *= os.path.exists(dbpath + "/score/file/" + dir + "/_desc.json")
    
    return bool(check)
  
  def getDBPath(self) -> str:
    return self.__dbpath
  
  def resetDBPath(self, my_db_path) -> None:
    if self.checkDBStructure(my_db_path):
      self.__dbpath = my_db_path
    else:
      print("DB structure not validated, DB path not changed")
      print("Please create your DB first")

