import os

from sanctus.db_base.cli_adapter import DataBaseCliAdapter
from constants import DEFAULT_LOCAL_DB_DIR

"""
List of commands:

fc: find composer [fmlyname, abbrname, year]
fp: find piece/arrangement/collection/template [title, opus, composer]

nc: create new composer
nw: create new piece/collection/arrangement/template
nwp: create new piece
nwc: create new collection
nwt: create new template

apc: add piece to collection

rc: remove composer
rw: remove piece/arrangement/collection/template

uc: update composer
uw: update piece/arrangement/collection/template

lc: list composer
lw: list all piece/collection/arrangement/template
lwp: list pieces
lwc: list collections
lwa: list arrangements
lwt: list templates

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
        while True:
          selected = input("Select an item [1-"+str(len(candidates))+"]: ")
          selected = int(selected.replace(" ","")) - 1
          if selected < len(candidates):
            return candidates[selected]
          else:
            print(str(selected) + " is out of range, please select again!")
    except:
      print("[Error] <_processSelectedNumber> cannot process")
      return {}
  
  # Commands
  def __fc(self, ):
    pass
  
  def __fw(self, ):
    pass
  
  def __nc(self, ):
    pass
  
  def __nwp(self, ):
    pass
  
  def __nwc(self, ):
    pass
  
  def __nwa(self, ):
    pass
  
  def __nwt(self, ):
    pass
  
  def __nw(self, ):
    pass
  
  def __apc(self, ):
    pass
  
  def __rc(self, ):
    pass
  
  def __rw(self, ):
    pass
  
  def __uc(self, ):
    pass
  
  def __uw(self, ):
    pass
  
  def __lc(self, ):
    pass
  
  def __lwp(self, ):
    pass
  
  def __lwc(self, ):
    pass
  
  def __lwa(self, ):
    pass
  
  def __lwt(self, ):
    pass
  
  def __lw(self, ):
    pass

  # End Commands
  
  def run(self) -> int:
    pass

if __name__ == "__main__":
  default_dbpath = os.path.abspath('~/Music/sanctus_db/data_v1')
  cmd = CommandLine(default_dbpath)
  cmd.run()