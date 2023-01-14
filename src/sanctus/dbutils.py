import os, sys, io, shutil
import string, json
import constants

class File_IO():
  def __init__(self) -> None:
    self.JSON_EXTENTION = ".json"
    pass

  def readJsonFileAsDict(self, fpath: str) -> dict:
    try:
      with open(fpath, "r") as f:
        return json.load(f)
    except ValueError as e:
      print("Error reading {}: {}".format(fpath, e))
      return None
  
  def readJsonFileAsStr(self, fpath: str) -> str:
    return json.dumps(self.getJsonFileAsDict(fpath))
  
  def writeJsonFile(self, jsonobj: dict, fpath: str) -> None:
    try:
      with open(fpath, "r") as f:
        json.dump(jsonobj, f)
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


class Composer_Info(File_IO):
  def __init__(self) -> None:
    super().__init__()
    pass

  def getByFamilyName(self, fmly_name: str) -> list:
    result = []
    try:
      first_letter = fmly_name.replace(" ","")[0].lower()
      # obtain json file name by family name initial
      file_to_search = first_letter + self.JSON_EXTENTION
      if os.path.exists(file_to_search):
        for item in self.readJsonFileAsDict(file_to_search):
          if fmly_name.lower() in item["FamilyName"].lower():
            return result.append(item)
      return []
    except ValueError as e:
      print("Error occured: {}; while querying {}".format(e, fmly_name))
  
  def getByNameCode(self, name_code: str) -> dict:
    try:
      for letter in string.ascii_lowercase:
        if os.path.exists(letter + self.JSON_EXTENTION):
          for item in self.readJsonFileAsDict(letter + self.JSON_EXTENTION):
            if name_code == item["NameCode1"] or name_code == item["NameCode2"]:
              return item
      return None
    except ValueError as e:
      print("Error occured: {}; while querying {}".format(e, name_code))

  def filterParticle(self, nametoken: list) -> list:
    # process family name particle
    try:
      filtered = list(map(lambda x: x.replace('von','v'), nametoken))
      filtered = list(map(lambda x: x.replace('van','v'), filtered))
      return filtered
    except RuntimeError as e:
      print("Error: {}".format(e))
  
  def getByAbbrName(self, abbr_name: str) -> dict:
    try:
      # Algorithm description:
      # 1) Replace dots and dash with whitespace
      processed = abbr_name.replace('.', ' ').replace('-', ' ')
      # 2) break the name into list, filter out empty elements
      nametoken = list(filter(lambda x : x != '', processed.split(' ')))
      # 2+) process family name particle
      nametoken = self.filterParticle(nametoken)

      # 3) case 1: the input name is correctly separated
      if len(nametoken) > 1:
        familyname = nametoken[-1].lower()
        # obtain json file name
        file_to_search = familyname[0] + self.JSON_EXTENTION
        
        # the name code is fusioned by initials
        namecode = ''.join(nametoken[:-1]).lower() + familyname

        if os.path.exists(file_to_search):
          for item in self.readJsonFileAsDict(file_to_search):
            if namecode == item["NameCode1"] or namecode == item["NameCode2"]:
              return item
      
      # 4) case 2: the input name is not separated
      elif len(nametoken) == 1:
        self.getByNameCode(processed)
      else:
        return None
    
    except ValueError as e:
      print("Error occured: {}; while querying {}".format(e, abbr_name))
