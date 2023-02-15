import os
from constants import DEFAULT_DB_DIR_PATH
from sanctus.db_base.db_composer import Composer_IO
from sanctus.db_base.db_metadata import Metadata_IO
from sanctus.db_base.db_score import Score_IO
from sanctus.db_base.dbutils import TextTools
"""
find composer [fmlyname, abbrname, year]
find piece/arrangement/collection/template [title, opus, composer]

add composer
add piece/collection/arrangement/template

rm composer
rm piece/arrangement/collection/template

update composer
update piece/arrangement/collection/template

ls composer
ls piece/collection/arrangement/template/all
"""

class DataBaseCliAdapterAbs:
  def __init__(self) -> None:
    pass

class DataBaseCliAdapter(DataBaseCliAdapterAbs, TextTools):
  def __init__(self, dbpath=DEFAULT_DB_DIR_PATH) -> None:
    self.__c = Composer_IO(dbpath)
    self.__m = Metadata_IO(dbpath)
    self.__s = Score_IO(dbpath)
  
  def __getCriteria(self, criteria: str) -> str:
    try:
      return str(criteria).replace(" ", "").replace("_", "").replace("-", "").lower()
    except:
      return ""
  
  def _processSelectedNumber(self, candidates: list, num: int) -> dict:
    choice = input("Choice: ")
    while not choice.isnumeric():
      print("Please input a number!")
      choice = input("Choice: ")
      if int(choice) < candidates.size() and int(choice) >= 0:
        return candidates[int(choice)]
  
  def _findComposerByYear(self, search_year_range: str) -> list:
    try:
      year_begin = search_year_range.split("-")[0]
      year_end = search_year_range.split("-")[1]
      # try int-str conversion to see if the format is correct
      year_begin = str(int(year_begin))
      year_end = str(int(year_end))
      
      result1 = self.__c._queryByYearRange(year_begin, year_end, year_type="Born")
      result2 = self.__c._queryByYearRange(year_begin, year_end, year_type="Died")
      
      result = []
      # iterate on the longer one, in order to get the overlap
      if len(result1) >= len(result2):
        for item in result1:
          if item in result2:
            result.append(item)
      else:
        for item in result2:
          if item in result1:
            result.append(item)
      return result
    except Exception as e:
      print("_findComposerByYear(): Exception occurred: {}".format(e))
      print("Year format Example: \"XXXX-XXXX\"")
      return []
    except RuntimeError as e:
      print("_findComposerByYear(): Error occurred: {}".format(e))
      print("Year format Example: \"XXXX-XXXX\"")
      return []
    except:
      print("_findComposerByYear(): Unknown problem")
      return []
      
  def findComposer(self, find_by: str, search_name: str) -> list:
    result = []
    criteria = self.__getCriteria(find_by)
    
    # family name
    if criteria in ["famname", "fmlyname", "familyname", "lastname", "family"]:
      result = self.__c.queryByFamilyName(search_name)
    
    # abbr name
    elif criteria in ["abbrname", "abbrivate", "abbr"]:
      result = self.__c.queryByAbbrName(search_name)

    # full name
    elif criteria in ["fullname", "full"]:
      name_list = search_name.replace("-"," ").split(" ")
      result = self.__c.queryByNameList(name_list)
    
    # year range
    elif criteria in ["year"]:
      result = self._findComposerByYear(search_name)
      
    else:
      print("Criteria \"{}\" is not valid".format(find_by))
      return []
    
    return result
  
  def findWork(self, find_by: str, search_string: str, work_type='all') -> list:
    result = []
    criteria = self.__getCriteria(find_by)
    if criteria in ["title", "subtitle", "subsubtitle", "ttl"]:
      result = self.__m.queryByTitle(search_string)
    elif criteria in ["opus", "op", "op."]:
      result = self.__m.queryByOpus(search_string)
    elif criteria in ["year", "y"]:
      result = self.__m.queryByYear(search_string)
    elif criteria in ["fname", "familyname", "fmlyname", "fmname", "composer"]:
      for item in self.__c.queryByFamilyName(search_string):
        composer_code = item["NameCode"]
        result = self.__m.queryByComposerCode(composer_code)
    elif criteria in ["abbrname", "composerabbrname", "composerabbr", "composername"]:
      for item in self.__c.queryByAbbrName(search_string):
        composer_code = item["NameCode"]
        result = self.__m.queryByComposerCode(composer_code)
    else:
      print("Warning: Invalid search criteria \"{}\"".format(search_string))
    
    return result
  
  def lsComposer(self) -> list:
    return self.__c.queryAllComposer()
  
  def lsWork(self, worktype='') -> list:
    result = []
    criteria = self.__getCriteria(worktype)
    if criteria in ["piece", "pieces"]:
      result = self.__m.queryByType("piece")
    
    elif criteria in ["collection", "collections"]:
      result = self.__m.queryByType("collection")
    
    elif criteria in ["arrangement", "arrangements"]:
      result = self.__m.queryByType("arrangement")
    
    elif criteria in ["template", "templates"]:
      result = self.__m.queryByType("template")
    
    elif criteria in ["all", ""]:
      result = self.__m.queryByType("piece")
      result += self.__m.queryByType("arrangement")
      result += self.__m.queryByType("template")
      result += self.__m.queryByType("collection")
    else:
      pass
    return result
  
  def addComposer(self,
                  given_name_list: list,
                  family_name_list: list,
                  born_year: str,
                  died_year: str,
                  known_as_name: str,
                  style: list,
                  wiki_link: str,
                  imslp_link: str) -> bool:
    return self.__c.createComposerEntry(
      given_name=given_name_list, 
      family_name=family_name_list,
      born_year=born_year,
      died_year=died_year,
      known_name=known_as_name,
      style=style,
      wiki_link=wiki_link,
      imlsp_link=imslp_link
    )
  
  def addWork(self,
              type_of_work: str,
              title: str,
              subtitle: str,
              subsubtitle: str,
              composer_name_code: str,
              opus: str,
              instrument_list: list) -> bool:
    return self.__m.createItem(
      type_of_work=type_of_work,
      title=title,
      subtitle=subsubtitle,
      subsubtitle=subsubtitle,
      composercode=composer_name_code,
      opus=opus,
      instruments=instrument_list
    )
  
  def updateComposer(self, name_code: str, dkey: str, new_val) -> bool:
    try:
      if dkey == "Style":
        if type(new_val) == list:
          return self.__c.updateComposerEntry(name_code=name_code, dkey=dkey, new_val=new_val)
        else:
          newval_list = str(new_val).replace(","," ").replace("-"," ").split(" ")
          newval_list = self._capitalizeList(self._filterEmptyStrFromList(newval_list))
          return self.__c.updateComposerEntry(name_code=name_code, dkey=dkey, new_val=newval_list)
      elif dkey == "Born":
        year = str(int(new_val))
        entry = self.__c.queryByNameCode(name_code)[0]
        status = self.__c.deleteComposerForce(name_code)
        return self.createComposerEntry(
          given_name=entry["GivenNameList"],
          family_name=entry["FamilyNameParticle"]+entry["FamilyNameList"],
          born_year=year,
          died_year=entry["Died"],
          known_name=entry["KnownAs"],
          style=entry["Style"],
          wiki_link=entry["wikiLink"],
          imlsp_link=entry["imslpLink"]
        )
      elif dkey == "Died":
        year = str(int(new_val))
        entry = self.__c.queryByNameCode(name_code)[0]
        status = self.__c.deleteComposerForce(name_code)
        return self.createComposerEntry(
          given_name=entry["GivenNameList"],
          family_name=entry["FamilyNameParticle"]+entry["FamilyNameList"],
          born_year=entry["Born"],
          died_year=year,
          known_name=entry["KnownAs"],
          style=entry["Style"],
          wiki_link=entry["wikiLink"],
          imlsp_link=entry["imslpLink"]
        )
      elif dkey == "FamilyNameList":
        newval_list = str(new_val).replace(","," ").replace("-"," ").split(" ")
        newval_list = self._capitalizeList(self._filterEmptyStrFromList(newval_list))
        return self.createComposerEntry(
          given_name=entry["GivenNameList"],
          family_name=entry["FamilyNameParticle"]+newval_list,
          born_year=entry["Born"],
          died_year=year,
          known_name=entry["KnownAs"],
          style=entry["Style"],
          wiki_link=entry["wikiLink"],
          imlsp_link=entry["imslpLink"]
        )
      elif dkey == "FamilyNameParticle":
        return self.createComposerEntry(
          given_name=entry["GivenNameList"],
          family_name=[str(new_val).lower()]+entry["FamilyNameList"],
          born_year=entry["Born"],
          died_year=year,
          known_name=entry["KnownAs"],
          style=entry["Style"],
          wiki_link=entry["wikiLink"],
          imlsp_link=entry["imslpLink"]
        )
      elif dkey == "GivenNameList":
        newval_list = str(new_val).replace(","," ").replace("-"," ").split(" ")
        newval_list = self._capitalizeList(self._filterEmptyStrFromList(newval_list))
        return self.createComposerEntry(
          given_name=newval_list,
          family_name=entry["FamilyNameParticle"]+entry["FamilyNameList"],
          born_year=entry["Born"],
          died_year=year,
          known_name=entry["KnownAs"],
          style=entry["Style"],
          wiki_link=entry["wikiLink"],
          imlsp_link=entry["imslpLink"]
        )
      elif dkey == "NameCode" or dkey == "NameCodeStrong":
        raise Exception("update forbidden on \"NameCode\"")
      else:
        return self.__c.updateComposerEntryAddKey(name_code=name_code, dkey=dkey, new_val=str(new_val))
      
    except RuntimeError as e:
      print("updateComposer(): Error - {}".format(e))
    except Exception as e:
      print("updateComposer(): Exception - {}".format(e))
    return False
  
  def updateWork(self, hashcode: str, dkey: str, new_val) -> bool:
    new_value = str(new_val)
    if dkey == "Instruments":
      if type(new_val) == list:
        pass
      else:
        new_val_list = str(new_val).replace(","," ").replace("."," ").split(" ")
        new_value = self._capitalizeList(self._filterEmptyStrFromList(new_val_list))
    elif dkey == "Hash":
      print("[Error] <updateWork> \"Hash\" update is forbidden")
      return False
    else:
      pass
    
    return self.__m.updateItem(hashcode=hashcode, dkey=dkey, new_val=new_value, addkey=True)

if __name__ == "__main__":
  pass