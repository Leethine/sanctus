import os

from sanctus.db_base.cli_adapter import DataBaseCliAdapter
from constants import DEFAULT_LOCAL_DB_DIR

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

class CommandLine():
  def __init__(self, dbpath=DEFAULT_LOCAL_DB_DIR) -> None:
    self.__cli = DataBaseCliAdapter(dbpath)
  
  def _processSelectedNumber(self, candidates: list) -> dict:
    try:
      if not candidates:
        return {}
      elif len(candidates) == 1:
        return candidates[0]
      else:
        selected = input("Select an item [1-"+str(len(candidates))+"]: ")
        selected = int(selected.replace(" ","")) - 1
        return candidates[selected]
    except:
      print("[Error] <_processSelectedNumber> cannot process")

  def run(self) -> int:
    pass

if __name__ == "__main__":
  default_dbpath = os.path.abspath('~/Music/sanctus_db/data_v1')
  cmd = CommandLine(default_dbpath)
  cmd.run()