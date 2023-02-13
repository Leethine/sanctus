import os
from db_base.db_composer import Composer_IO
from db_base.db_metadata import Metadata_IO
from db_base.db_score import Score_IO

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

class DataBaseCliAdapter():
  def __init__(self, dbpath='~/') -> None:
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
      result2 = self.__c._queryByYearRange(year_begin, year_end, year_type="Dead")
      
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
    result = []
  
  def lsWork(self, worktype: str) -> list:
    result = []
    criteria = self.__getCriteria(worktype)
    if criteria in ["piece", "pieces"]:
      pass
    elif criteria in ["collection", "collections"]:
      pass
    elif criteria in ["arrangement", "arrangements"]:
      pass
    elif criteria in ["template", "templates"]:
      pass
    else:
      pass
  
  def findInteractive(self) -> dict:
    pass
  
  def addComposerInteractive(self) -> bool:
    pass
  
  def addWorkInteractive(self) -> bool:
    pass
  
  def updateComposerInteractive(self) -> bool:
    pass
  
  def updatePieceInteractive(self) -> bool:
    pass

if __name__ == "__main__":
  default_dbpath = os.path.abspath('~/Music/sanctus_db/data_v1')
  cmd = DataBaseCliAdapter(default_dbpath)