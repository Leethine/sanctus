import sys, os, json
import sanctus.constants as constants
from sanctus.db_base.dbutils import File_IO, TextTools

class Composer_IO(File_IO, TextTools):
  def __init__(self, db_root=constants.DEFAULT_LOCAL_DB_DIR) -> None:
    super().__init__(db_root)
    self._COMPOSER_ROOT = "composer/"
    self._INFO_DIR = self._COMPOSER_ROOT + "info/"
    self._ICON_DIR = self._COMPOSER_ROOT + "icon/"
    self._BIOG_DIR = self._COMPOSER_ROOT +"biography/"
    if not self._checkDirectory():
      print("[WARNING] Composer directory invalid")
      raise("Directory invalid")

  def _filterNameParticle(self, family_name_list: list) -> dict:
    try:
      # filter 'von', 'van', 'de', 'da'
      results = self._separateStrFromList(family_name_list, ['von','van','de','da'])
      if len(results["target"]) == 1:
        return {"FamilyName": results["filtered"], "FamilyNameParticle": results["target"][0]}
      elif len(results["target"]) == 0:
        return {"FamilyName": results["filtered"], "FamilyNameParticle": ""}
      else:
        raise Exception("Only one name particle is allowed")
    except Exception as excp:
      print("_filterNameParticle(): {}".format(excp))
    except RuntimeError as e:
      print("_filterNameParticle(): {}".format(e))

  def _filterNamePostfix(self, family_name_list: list) -> dict:
    try:
      # filter 'jr', 'jr.', 'ii', 'iii'
      list_of_common_postfix = ['jr', 'jr.','ii','iii']
      results = self._separateStrFromList(family_name_list, list_of_common_postfix)
      if len(results["target"]) == 1:
        return {"FamilyName": results["filtered"], "NamePostfix": results["target"][0]}
      elif len(results["target"]) == 0:
        return {"FamilyName": results["filtered"], "NamePostfix": ""}
      else:
        raise Exception("Only one name postfix is allowed")
    except Exception as excp:
      print("_filterNamePostfix(): {}".format(excp))
    except RuntimeError as e:
      print("_filterNamePostfix(): {}".format(e))

  def _compNameCode(self, given_name_list: list, family_name_list: list,
                    family_name_particle='', name_postfix='') -> str:
    result = []
    try:
      # given name initials
      for item in given_name_list:
        first_letter = item[0]
        result.append(first_letter)
      
      # append family name particle
      result.append(family_name_particle)
      
      # full family name
      for item in family_name_list:
        result.append(item)
      # first letter of first family name
      first_letter_fn = family_name_list[0][0]

      # append name postfix while removing '-' and '.'
      result.append(name_postfix.replace('-','').replace('.',''))

      # filter empty string and convert to lower case
      processed = self._lowercaseList(self._filterEmptyStrFromList(result))

      return first_letter_fn.upper() + '-' + '_'.join(processed)

    except RuntimeError as e:
      print("_compNameCode(): Error: {}".format(e))
      return ""
  
  def _compYearHash(self, born_year='?', died_year='?') -> int:
    born = str(born_year)
    died = str(died_year)
    
    if not born.isnumeric() or not len(born) == 4:
      born = int(1516)
    else:
      born = int(born_year)
    
    if not died.isnumeric() or not len(died) == 4:
      died = int(2021)
    else:
      died = int(died_year)
    
    if born < 100 or died < 100:
      born = int(1516)
      died = int(2021)
    
    # calculate the hash
    return (born + died) % int((born / 100))

  def _createNewInfoDict(self, given_name_input: list, family_name_input: list) -> dict:
    try:
      # covert to lower case
      given_name = self._lowercaseList(given_name_input)
      family_name = self._lowercaseList(family_name_input)
      
      # filter out particle
      filtered_dict1 = self._filterNameParticle(family_name)
      particle = filtered_dict1["FamilyNameParticle"]
      
      # filter out postfix
      filtered_dict2 = self._filterNamePostfix(filtered_dict1["FamilyName"])
      postfix = filtered_dict2["NamePostfix"]
      family_name = filtered_dict2["FamilyName"]

      # compute composer namecode
      namecode = self._compNameCode(given_name, family_name, \
                                    family_name_particle=particle, \
                                    name_postfix=postfix)
      
      full_name_list = [item for item in given_name] \
                    + [particle] \
                    + [item for item in family_name] \
                    + [postfix.capitalize()]
      
      # capitalize and filter empty string
      full_name_list = self._filterEmptyStrFromList(full_name_list)
      full_name_list = self._capitalizeList(full_name_list)

      given_name = self._capitalizeList(self._filterEmptyStrFromList(given_name))
      family_name = self._capitalizeList(self._filterEmptyStrFromList(family_name))
      
      new_entry = {
        "FullName": ' '.join(full_name_list),
        "KnownAs": ' '.join(full_name_list),
        "GivenNameList": given_name,
        "FamilyNameParticle": particle,
        "FamilyNameList": family_name,
        "NamePostfix": postfix,
        "NameCode": namecode,
        "NameCodeStrong": namecode,
        "Born": "?",
        "Died": "?",
        "Style": [],
        "wikiLink": "",
        "imslpLink": ""
      }
      return new_entry
    except RuntimeError as e:
      print("_createNewInfoDict(): Error: {}".format(e))
      return {}

  def _updateEntry(self, orig_entry: dict, dict_key: str, new_val = '') -> dict:
    if dict_key in orig_entry.keys():
      orig_entry[dict_key] = new_val
    return orig_entry
  
  def _updateComposerYears(self, orig_entry: dict, year_born='?', year_died='?') -> dict:
    year1 = str(year_born)
    year2 = str(year_died)
    if not year1.isnumeric():
      year1 = "?"
    if not year2.isnumeric():
      year2 = "?"
    
    orig_entry["Born"] = year1
    orig_entry["Died"] = year2

    orig_entry["NameCodeStrong"] = orig_entry["NameCode"] \
                                 + "_" \
                                 + str(self._compYearHash(year1, year2))

    return orig_entry

  def _updateComposerKnwonName(self, orig_entry: dict, known_name: str) -> dict:
    return self._updateEntry(orig_entry, "KnownAs", new_val=known_name)
  
  def _updateAddComposerStyle(self, orig_entry: dict, new_style: str) -> dict:
    orig_entry["Style"].append(str(new_style))
    return orig_entry
  
  def _updateClearComposerStyle(self, orig_entry: dict) -> dict:
    orig_entry["Style"] = []
    return orig_entry

  def _updateComposerStyle(self, orig_entry: dict, style=[]) -> dict:
    if type(orig_entry["Style"]).__name__ == 'list':
      orig_entry["Style"] = style
    elif type(orig_entry["Style"]).__name__ == 'str':
      orig_entry["Style"].append(style)
    else:
      raise Exception("style={} - Type: {} not supported".format(style, type(style).__name__))
    return orig_entry

  def _updateComposerWikiLink(self, orig_entry: dict, wiki_link: str) -> dict:
    orig_entry["wikiLink"] = wiki_link
    return orig_entry
  
  def _updateComposerImslpLink(self, orig_entry: dict, ismlp_link: str) -> dict:
    orig_entry["imslpLink"] = ismlp_link
    return orig_entry

  def _getPartitionFilePath(self, name_code: str) -> str:
    if len(name_code) != 0:
      return self._INFO_DIR \
      + constants.COMPOSER_NAME_PARTITION_MAP[name_code[0]] \
      + self.JSON_EXTENTION
    else:
      raise Exception("Exception: NameCode is empty.")
  
  def _getAllInfoJsonFilePath(self) -> list:
    list_files = os.listdir(self._INFO_DIR)
    list_json = []
    for f in list_files:
      if f.split(".")[-1] != "json":
        pass
      elif f == "_desc.json":
        pass
      else:
        list_json.append(f)
    return list_json

  def queryAllComposer(self, dkey='') -> list:
    try:
      result = []
      for jsonfile in self._getAllInfoJsonFilePath():
        for item in self.readJsonFileAsObj(self._INFO_DIR + jsonfile):
          if not dkey:
            result.append(item)
          else:
            result.append(item[dkey])
      return result
    except RuntimeError as e:
      print("queryAllComposer(): Error: {}".format(e))
      return []
    except Exception as excp:
      print("queryAllComposer(): Exception: {}".format(excp))
      return []
  
  def queryByNameCode(self, name_code: str) -> list:
    try:
      jsonfile_path = self._getPartitionFilePath(name_code)
      
      result = []
      if not os.path.exists(jsonfile_path):
        return result
      
      for item in self.readJsonFileAsObj(jsonfile_path):
        if item["NameCode"] == name_code:
          result.append(item)
      return result
    except RuntimeError as e:
      print("queryByNameCode(): Error: {}".format(e))
      return []
    except Exception as e:
      print("queryByNameCode(): Exception: {}".format(e))
      return []

  def queryByFamilyName(self, family_name: str) -> list:
    try:
      jsonfile_path = self._getPartitionFilePath(family_name[0])
      result = []

      if not os.path.exists(jsonfile_path):
        return result
      
      for item in self.readJsonFileAsObj(jsonfile_path):
        if family_name.capitalize() in item["FamilyNameList"]:
          result.append(item)
      return result
    except RuntimeError as e:
      print("queryByFamilyName(): Error: {}".format(e))
      return []
    except Exception as excp:
      print("queryByFamilyName(): Exception: {}".format(excp))
      return []

  def queryByAbbrName(self, abbr_name: str) -> list:
    try:
      # prepare search candidates
      abbr_name_list = abbr_name.lower().replace('.',' ').replace('-',' ').split(' ')
      abbr_name_list = self._filterEmptyStrFromList(abbr_name_list)
      given_name_initials = list(filter(lambda x: len(x) == 1, abbr_name_list))
      family_name_list = list(filter(lambda x: len(x) != 1, abbr_name_list))
      family_name_particle = self._filterNameParticle(family_name_list)["FamilyNameParticle"]
      family_name_list = self._filterNameParticle(family_name_list)["FamilyName"]

      # go to family name partition
      first_letter = family_name_list[0][0]
      jsonfile_path = self._getPartitionFilePath(first_letter)
      result = []

      if not os.path.exists(jsonfile_path):
        return result

      # fuzzy match family name and initials
      for item in self.readJsonFileAsObj(jsonfile_path):
        match_gn = False
        match_particle = False
        match_fn = False
        if family_name_particle == "" or family_name_particle == item["FamilyNameParticle"]:
          match_particle = True
        
        for gn in item["GivenNameList"]:
          for init in given_name_initials:
            if init.upper() == gn[0]:
              match_gn = True
              break
        
        for fn in item["FamilyNameList"]:
          for fn_input in family_name_list:
            if fn_input.capitalize() == fn:
              match_fn= True
              break
        
        if match_gn and match_particle and match_fn:
          result.append(item)
      
      return result
    
    except RuntimeError as e:
      print("queryByAbbrName(): Error: {}".format(e))
      return []
    except Exception as excp:
      print("queryByAbbrName(): Exception: {}".format(excp))
      return []

  def queryByNameList(self, name_list: list) -> list:
    try:
      name_list = self._capitalizeList(name_list)
      result = []
      for jsonfile in self._getAllInfoJsonFilePath():
        for item in self.readJsonFileAsObj(self._INFO_DIR + jsonfile):
          matched = False
          candidate = item["GivenNameList"] + item["FamilyNameList"]
          for name in name_list:
            for can in candidate:
              if name == can:
                matched = True
                break
          if matched:
            result.append(item)
      return result
    except RuntimeError as e:
      print("queryByNameList(): Error: {}".format(e))
      return []
    except Exception as excp:
      print("queryByNameList(): Exception: {}".format(excp))
      return []

  def _queryByYearRange(self, year_low: str, year_high: str, year_type='Born') -> list:
    try:
      result = []
      
      # preprocess the input
      from_year = str(year_low)
      to_year = str(year_high)
      if not from_year.isnumeric() and not to_year.isnumeric():
        return result
      elif from_year.isnumeric() and not to_year.isnumeric():
        to_year = 2100
        from_year = int(from_year)
      elif not from_year.isnumeric() and to_year.isnumeric():
        from_year = 1000
        to_year = int(to_year)
      else:
        from_year = int(from_year)
        to_year = int(to_year)

      for jsonfile in self._getAllInfoJsonFilePath():
        for item in self.readJsonFileAsObj(self._INFO_DIR + jsonfile):
          if item["Born"].isnumeric() and item["Died"].isnumeric():
            candidate_year = int(item[year_type])
            
            if candidate_year > from_year and candidate_year < to_year:
              result.append(item)
      
      return result
    except RuntimeError as e:
      print("queryByYearRange(): Error: {}".format(e))
      return []
    except Exception as excp:
      print("queryByYearRange(): Exception: {}".format(excp))
      return []

  def queryByBornYearRange(self, year_low: str, year_high: str) -> list:
    return self._queryByYearRange(year_low, year_high, year_type='Born')

  def queryByDiedYearRange(self, year_low: str, year_high: str) -> list:
    return self._queryByYearRange(year_low, year_high, year_type='Died')
  
  def isComposerInDB(self, name_code) -> bool:
    if not self.queryByNameCode(name_code):
      return False
    else:
      return True

  def createComposerEntry(self, given_name: list, family_name: list, \
                          born_year: str, died_year: str, known_name='',
                          style=[], wiki_link='', imlsp_link='') -> bool:
    try:
      entry = self._createNewInfoDict(given_name, family_name)
      entry = self._updateComposerYears(entry, born_year, died_year)
      entry = self._updateComposerKnwonName(entry, known_name)
      entry = self._updateComposerStyle(entry, style)
      entry = self._updateComposerWikiLink(entry, wiki_link)
      entry = self._updateComposerImslpLink(entry, imlsp_link)

      # The partition is obtained by the first letter of family name
      jsonfile_path = self._getPartitionFilePath(entry["NameCode"])
      if not os.path.exists(jsonfile_path):
        # create new json (list) file
        self.createNewJsonFile([], jsonfile_path)
      
      # check if conflicts found
      if not self.queryByNameCode(entry["NameCode"]):
        # append new entry to json file
        newjsonobj = self.readJsonFileAsObj(jsonfile_path)
        newjsonobj.append(entry)
        self.writeJsonFile(newjsonobj, jsonfile_path + "~")

        # finish writing, move file
        self.fmoveReplace(jsonfile_path + "~", jsonfile_path)
        print("[INFO] Created {}".format(entry["NameCode"]))
        return True
      else:
        pass #TODO handle name conflict
        return False

    except RuntimeError as e:
      print("createComposerEntry(): Error: {}".format(e))
      return False
    except Exception as excp:
      print("createComposerEntry(): Exception: {}".format(excp))
      return False

  def deleteComposerForce(self, name_code: str) -> bool:
    try:
      for jsonfile in self._getAllInfoJsonFilePath():
        curr_fpath = self._INFO_DIR + jsonfile
        curr_jsonobj = self.readJsonFileAsObj(curr_fpath)
        for item in curr_jsonobj:
          if item["NameCode"] == name_code:
            curr_jsonobj.remove(item)
            # write to new file, then replace json file
            new_fpath = curr_fpath + "~"
            self.writeJsonFile(curr_jsonobj, new_fpath)
            self.fmoveReplace(new_fpath, curr_fpath)
            print("[INFO] Removed {}".format(name_code))
    except RuntimeError as e:
      print("removeComposerForce(): Error: {}".format(e))
      return False
    except Exception as excp:
      print("removeComposerForce(): Exception: {}".format(excp))
      return False
      
  def deleteComposer(self, name_code: str) -> bool:
    try:
      query = self.queryByNameCode(name_code)
      if not query:
        return False
      elif len(query) > 1:
        raise Exception("Multiple composers with the same NameCode exists in DB: {}".format(name_code))
      else:
        self.deleteComposerForce(name_code)
    except RuntimeError as e:
      print("removeComposer(): Error: {}".format(e))
      return False
    except Exception as excp:
      print("removeComposer(): Exception: {}".format(excp))
      return False

  def updateComposerEntry(self, name_code: str, dkey: str, new_val) -> bool:
    try:
      query = self.queryByNameCode(name_code)
      if not query:
        return False
      elif len(query) > 1:
        raise Exception("Multiple composers with the same NameCode exists in DB: {}".format(name_code))
      else:
        entry = query[0]
        if dkey not in entry.keys():
          raise Exception("updateComposerEntry(): {} is not a valid key".format(dkey))
        # only allow updating "safe" keys
        elif dkey not in ['KnownAs', 'Style', 'wikiLink', 'imslpLink', 'OpusSystem']:
          raise Exception("Key \"{}\" is protected, cannot be updated".format(dkey))
        else:
          entry[dkey] = new_val
          print("[INFO] Updated {}: {} = {}".format(name_code, dkey, new_val))
          return True
    except RuntimeError as e:
      print("updateComposerEntry(): Error: {}".format(e))
      return False
    except Exception as excp:
      print("updateComposerEntry(): Exception: {}".format(excp))
      return False

  def updateComposerEntryAddKey(self, name_code: str, dkey: str, new_val) -> bool:
    try:
      query = self.queryByNameCode(name_code)
      if not query:
        return False
      elif len(query) > 1:
        raise Exception("Multiple composers with the same NameCode exists in DB: {}".format(name_code))
      else:
        entry = query[0]
        if dkey in ["GivenNameList", "FamilyNameParticle", "FamilyNameList", 
                    "NamePostfix", "NameCode", "NameCodeStrong", "Born","Died"]:
          raise Exception("cannot update, \"{}\" is a protected key".format(dkey))
        # only allow updating "safe" keys
        else:
          entry[dkey] = new_val
          print("[INFO] Updated {}: {} = {}".format(name_code, dkey, new_val))
          return True
    except RuntimeError as e:
      print("updateComposerEntry(): Error: {}".format(e))
      return False
    except Exception as excp:
      print("updateComposerEntry(): Exception: {}".format(excp))
      return False
    