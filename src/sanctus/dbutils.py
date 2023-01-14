import os, sys, io, shutil
import string, json
import constants

class File_IO():
  def __init__(self, db_root=constants.DEFAULT_LOCAL_DB_DIR) -> None:
    self.JSON_EXTENTION = ".json"
    self.DB_ROOT = os.path.abspath(db_root)
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
  
  def writeJsonFile(self, jsonobj: dict, fpath: str) -> None:
    try:
      with open(fpath, "w") as f:
        json.dump(jsonobj, f, indent=2)
    except ValueError as e:
      print("Error writing {}: {}".format(fpath, e))

  def writeJsonFile(self, jsonobj: list, fpath: str) -> None:
    try:
      with open(fpath, "w") as f:
        json.dump(jsonobj, f, indent=2)
    except ValueError as e:
      print("Error writing {}: {}".format(fpath, e))
  
  def createNewJsonFile(self, jsonobj: list, fpath: str) -> None:
    try:
      if not os.path.exists(fpath):
        with open(fpath, "w+") as f:
          json.dump(jsonobj, f)
      else:
        print("Warning: file exists: {} -> nothing to do".format(fpath))
    except ValueError as e:
      print("Error creating {}: {}".format(fpath, e))

  def createNewJsonFile(self, jsonobj: dict, fpath: str) -> None:
    try:
      if not os.path.exists(fpath):
        with open(fpath, "w+") as f:
          json.dump(jsonobj, f)
      else:
        print("Warning: file exists: {} -> nothing to do".format(fpath))
    except ValueError as e:
      print("Error creating {}: {}".format(fpath, e))

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
      shutil.move(from_path, to_path, copy_function=shutil.copy2)
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


class Composer_IO(File_IO):
  def __init__(self, db_root=constants.DEFAULT_LOCAL_DB_DIR) -> None:
    super().__init__(db_root=db_root)
    self.INFO_DIR = "info/"
    self.OEUVRE_DIR = "oeuvre/"
    self.ICON_DIR = "icon/"
    self.BIOG_DIR = "biography/"
    
    try:
      if self.checkDirectory():
        os.chdir("composer")
      else:
        raise Exception("Composer_IO(): Directory Error: " + db_root)
    except Exception as excp:
      print(excp)

  def checkDirectory(self) -> bool:
    if self.getCWD() == os.path.abspath(os.path.curdir):
      return True
    else:
      return False

  def getByFamilyName(self, fmly_name: str) -> list:
    result = []
    try:
      first_letter = fmly_name.replace(" ","")[0].lower()
      # obtain json file name by family name initial
      file_to_search = self.INFO_DIR + first_letter + self.JSON_EXTENTION
      if os.path.exists(file_to_search):
        for item in self.readJsonFileAsObj(file_to_search):
          if fmly_name.lower() in item["FamilyName"].lower():
            return result.append(item)
      return []
    except ValueError as e:
      print("Error occured: {}; while querying {}".format(e, fmly_name))
  
  def getByNameCode(self, name_code: str) -> dict:
    try:
      for letter in string.ascii_lowercase:
        file_to_search = self.INFO_DIR + letter + self.JSON_EXTENTION
        if os.path.exists(file_to_search):
          for item in self.readJsonFileAsObj(file_to_search):
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
      print("filterParticle(): Error: {}".format(e))
  
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
        file_to_search = self.INFO_DIR + familyname[0] + self.JSON_EXTENTION
        
        # the name code is fusioned by initials
        namecode = ''.join(nametoken[:-1]).lower() + familyname

        if os.path.exists(file_to_search):
          for item in self.readJsonFileAsObj(file_to_search):
            if namecode == item["NameCode1"] or namecode == item["NameCode2"]:
              return item
      
      # 4) case 2: the input name is not separated
      elif len(nametoken) == 1:
        self.getByNameCode(processed)
      else:
        return None
    
    except ValueError as e:
      print("Error occured: {}; while querying {}".format(e, abbr_name))
  
  def isComposerInDB(self, namecode) -> bool:
    pass
  
  def createNewInfoEntry(self, family_name: str, first_name: str, \
                           second_name: str, third_name: str, \
                           birth_year: str, death_year: str, \
                           family_name_particle='', \
                           style=[], wiki_link='') -> None:
    try:
      # ignore empty list element
      full_name = [first_name, second_name, third_name, family_name_particle, family_name]
      full_name = list(filter(lambda x: x != '', full_name))
      
      composer_item = { \
        "FullName": ' '.join(full_name), \
        "FirstName": first_name, \
        "SecondName": second_name, \
        "ThirdName": third_name, \
        "FamilyNameParticle": family_name_particle, \
        "FamilyName": family_name, \
        "NameCode1": "", \
        "NameCode2": "", \
        "Born": str(birth_year), \
        "Death": str(death_year), \
        "Style": style, \
        "wikiLink": wiki_link \
      }

      composer_item["NameCode1"] = composer_item["FirstName"][:1] \
                                 + composer_item["SecondName"][:1] \
                                 + composer_item["ThirdName"][:1] \
                                 + composer_item["FamilyNameParticle"][:-1] \
                                 + composer_item["FamilyName"]

      composer_item["NameCode1"] = composer_item["NameCode1"].lower()

      composer_item["NameCode2"] = composer_item["FirstName"][:1] \
                                 + composer_item["SecondName"][:1] \
                                 + composer_item["ThirdName"][:1] \
                                 + composer_item["FamilyName"]
      
      composer_item["NameCode2"] = composer_item["NameCode2"].lower()
      
      file_to_add = self.INFO_DIR + family_name[0].lower() + self.JSON_EXTENTION

      # if partition not exist, create new partition first
      if not os.path.exists(file_to_add):
        self.createNewJsonFile([], file_to_add)
      list_composer = self.readJsonFileAsObj(file_to_add)

      # Write to new file
      list_composer.append(composer_item)
      self.writeJsonFile(list_composer, file_to_add + "~")
      self.fmoveReplace(file_to_add + "~", file_to_add)

    except ValueError as e:
      print("Failde to create new entry. Error occured: {}".format(e))

