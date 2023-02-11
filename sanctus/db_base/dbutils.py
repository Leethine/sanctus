import os, sys, io, shutil
import string, json
import sanctus.constants as constants

class TextTools():
  def __init__(self) -> None:
    pass

  def __do_nothing(self, inputArg):
    return inputArg
  
  def _separateStrFromList(self, inputList: list, targetList: list) -> dict:
    target = list(filter(lambda x: x in targetList, inputList))
    filtered = list(filter(lambda x: x not in targetList, inputList))
    return {"filtered": filtered, "target": target}

  def _filterEmptyStrFromList(self, inputList: list) -> list:
    return list(filter(lambda x: x != '', inputList))
  
  def _filterExtraSpaceFromStr(self, inputStr: str) -> str:
    tokenized = inputStr.split(' ')
    filtered = list(filter(lambda x: x != '', tokenized))
    return ' '.join(filtered)

  def __processListGeneric(self, inputList: list, my_func=__do_nothing) -> list:
    return [my_func(item) for item in inputList]
  
  def __processStrGeneric(self, inputStr: str, my_func=__do_nothing) -> str:
    tokenized = inputStr.split(' ')
    processed = [my_func(item) for item in tokenized]
    filtered = list(filter(lambda x: x != '', processed))
    return ' '.join(filtered)
  
  def _capitalizeList(self, inputList: list) -> list:
    return self.__processListGeneric(inputList, str.capitalize)

  def _capitalizeStr(self, inputStr: str) -> str:
    self.__processStrGeneric(inputStr, str.capitalize)
  
  def _lowercaseList(self, inputList: list) -> list:
    return self.__processListGeneric(inputList, str.lower)
  
  def _lowercaseStr(self, inputStr: str) -> str:
    return self.__processStrGeneric(inputStr, str.lower)


class DB_Connect():
  def __init__(self, my_db_path=constants.DEFAULT_LOCAL_DB_DIR) -> None:
    self.DB_ROOT = os.path.abspath(my_db_path)
    if not self._checkDBStructure(self.DB_ROOT):
      print("DB structure is invalid, please recreate DB, or check your path")
      exit(constants.DB_NON_VALID_ERR)

  def _checkDirectory(self) -> bool:
    if self.getCWD() == os.path.abspath(os.path.curdir):
      return True
    else:
      return False

  def _checkDBStructure(self, dbpath_to_check: str) -> bool:
    dbpath = os.path.abspath(dbpath_to_check)

    check = 1

    # composer
    check *= os.path.exists(dbpath + "/composer")
    check *= os.path.exists(dbpath + "/composer/info")
    check *= os.path.exists(dbpath + "/composer/icon")
    check *= os.path.exists(dbpath + "/composer/biography")
    
    # metadata
    check *= os.path.exists(dbpath + "/metadata")
    check *= os.path.exists(dbpath + "/metadata/arrangement")
    check *= os.path.exists(dbpath + "/metadata/collection")
    check *= os.path.exists(dbpath + "/metadata/piece")
    check *= os.path.exists(dbpath + "/metadata/template")
    
    # score
    check *= os.path.exists(dbpath + "/score")
    file_dir = list(string.digits + "abcdef")
    for dir in file_dir:
      check *= os.path.exists(dbpath + "/score/" + dir)
    
    return bool(check)
  
  def getDBPath(self) -> str:
    return self.DB_ROOT
  
  def resetDBPath(self, my_db_path) -> None:
    if self._checkDBStructure(my_db_path):
      self.DB_ROOT = my_db_path
    else:
      print("DB structure not validated, DB path not changed")
      print("Please create your DB first")


class File_IO(DB_Connect):
  def __init__(self, db_root=constants.DEFAULT_LOCAL_DB_DIR) -> None:
    super().__init__(db_root)
    self.JSON_EXTENTION = ".json"
    os.chdir(self.DB_ROOT)

  def readJsonFileAsObj(self, fpath: str):
    #TODO: return type (list | dict)
    try:
      with open(fpath, "r") as f:
        return json.load(f)
    except ValueError as e:
      print("Error reading {}: {}".format(fpath, e))
      return None
  
  def readJsonFileAsStr(self, fpath: str) -> str:
    return json.dumps(self.readJsonFileAsObj(fpath))
  
  def getCWD(self) -> str:
    try:
      if os.path.exists("_desc.json"):
        cwd = self.readJsonFileAsObj("_desc.json")["cwd"].replace("$ROOT", self.DB_ROOT)
        if cwd == os.path.abspath(os.path.curdir):
          return cwd
        else:
          raise Exception("Error: curdir does not match _desc.json")
          print("{} ==> {}".format(cwd, os.path.curdir))
      else:
        raise Exception("Error: '_desc.json' file does not exist")
        print("curdir: {}".format(os.path.abspath(os.path.curdir)))
    except RuntimeError as e:
      print("getCWD(): Error: {}".format(e))
    except Exception as excp:
      print("getCWD(): Error: {}".format(excp))
  
  def writeRawJsonFile(self, jsonobj: dict, fpath: str, indent=None) -> None:
    try:
      with open(fpath, "w") as f:
        json.dump(jsonobj, f, indent=indent)
    except ValueError as e:
      print("writeJsonFile(): Error writing {}: {}".format(fpath, e))
  
  def writeRawJsonFile(self, jsonobj: list, fpath: str, indent=None) -> None:
    try:
      with open(fpath, "w") as f:
        json.dump(jsonobj, f, indent=indent)
    except ValueError as e:
      print("writeJsonFile(): Error writing {}: {}".format(fpath, e))

  def writeJsonFile(self, jsonobj: dict, fpath: str) -> None:
    self.writeRawJsonFile(jsonobj, fpath, indent=2)

  def writeJsonFile(self, jsonobj: list, fpath: str) -> None:
    self.writeRawJsonFile(jsonobj, fpath, indent=2)
  
  def createNewJsonFile(self, jsonobj: list, fpath: str) -> None:
    try:
      if not os.path.exists(fpath):
        with open(fpath, "w+") as f:
          json.dump(jsonobj, f)
      else:
        print("createNewJsonFile(): Warning: file exists: {}".format(fpath))
    except ValueError as e:
      print("createNewJsonFile(): Error creating {}: {}".format(fpath, e))

  def createNewJsonFile(self, jsonobj: dict, fpath: str) -> None:
    try:
      if not os.path.exists(fpath):
        with open(fpath, "w+") as f:
          json.dump(jsonobj, f)
      else:
        print("createNewJsonFile(): Warning: file exists: {}".format(fpath))
    except ValueError as e:
      print("createNewJsonFile(): Error creating {}: {}".format(fpath, e))

  def readFileLines(self, fpath: str) -> list:
    try:
      with open(fpath, "r") as f:
        return f.readlines()
    except ValueError as e:
      print("readFileLines(): Error reading {}: {}".format(fpath, e))
  
  def readFileAsStr(self, fpath: str) -> str:
    try:
      with open(fpath, "r") as f:
        return f.read()
    except ValueError as e:
      print("readFileAsStr(): Error reading {}: {}".format(fpath, e))
  
  def fcopyReplace(self, from_path: str, to_path: str) -> str:
    try:
      if os.path.exists(to_path):
        os.remove(to_path)
      shutil.copy2(from_path, to_path)
    except RuntimeError as e:
      print("fcopyReplace(): Error during fcopy: {}".format(e))
  
  def fcopyNoReplace(self, from_path: str, to_path: str) -> str:
    try:
      if os.path.exists(to_path):
        #print("fcopy: dst file exists, abort.")
        pass
      else:
        shutil.copy2(from_path, to_path)
    except RuntimeError as e:
      print("fcopyNoReplace(): Error during fcopy: {}".format(e))
  
  def fmoveReplace(self, from_path: str, to_path: str) -> str:
    try:
      shutil.move(from_path, to_path, copy_function=shutil.copy2)
    except RuntimeError as e:
      print("fmoveReplace(): Error during fmove: {}".format(e))

  def fmoveNoReplace(self, from_path: str, to_path: str) -> str:
    try:
      if os.path.exists(to_path):
        #print("fmove: dst file exists, abort.")
        pass
      else:
        shutil.move(from_path, to_path, copy_function=shutil.copy2())
    except RuntimeError as e:
      print("fmoveNoReplace(): Error during fmove: {}".format(e))

