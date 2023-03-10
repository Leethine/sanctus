import os, sys
import re

from sanctus.db_base.cli_adapter import DataBaseCliAdapter
from sanctus.constants import DEFAULT_LOCAL_DB_DIR
from sanctus.tools.json_printer import JsonPrinter
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
    self.__json_print = JsonPrinter()
    
  def _processInput(self, prompt: str) -> str:
    search_str = input(prompt)
    search_str = re.sub('[^a-zA-Z0-9_\.\s]', '', search_str)
    return search_str
  
  def _processSelectedNumber(self, candidates: list) -> dict:
    try:
      if not candidates:
        return {}
      elif len(candidates) == 1:
        return candidates[0]
      else:
        while True:
          selected = input("> Select an item [1-"+str(len(candidates))+"]: ")
          selected = int(re.sub('\D', '', selected)) - 1
          if selected < len(candidates):
            return candidates[selected]
          else:
            print(str(selected) + " is out of range, please select again!")
    except:
      print("[Error] <_processSelectedNumber> cannot process")
      return {}
  
  # Commands
  def __fc(self) -> list:
    found = []
    search = self._processInput("Find composer:\n>> ")
    if "." in search:
      found = self.__cli.findComposer("abbr", search_name=search)
    elif "1" in search or "2" in search:
      found = self.__cli.findComposer("year", search_name=search)
    else:
      # note: disable full name search
      found = self.__cli.findComposer("fmlyname", search_name=search) \
            + self.__cli.findComposer("abbr", search_name=search)
    return found
  
  def __fw(self) -> list:
    search = self._processInput("Find work:\n>> ")
    
    # in case of searching by opus
    by_opus = False
    for i in "0123456789":
      if i in search:
        by_opus = True
        break
    if by_opus:
      return self.__cli.findWork("opus", search_string=search)
    
    # search by composer family name
    by_composer = self.__cli.findComposer(find_by="fmlyname", search_name=search)
    if by_composer:
      print(by_composer)
      return self.__cli.findWork(find_by='fname', search_string=search)

    # in the end, try finding by title
    found = self.__cli.findWork(find_by='title', search_string=search)
    if found:
      return found
    
    return []
    
  def __fwp(self):
    pass
  
  def __fwc(self):
    pass
  
  def __fwa(self):
    pass
  
  def __fwt(self):
    pass
  
  def __nc(self):
    pass
  
  def __nwp(self):
    pass
  
  def __nwc(self):
    pass
  
  def __nwa(self):
    pass
  
  def __nwt(self):
    pass
  
  def __nw(self):
    pass
  
  def __apc(self):
    pass
  
  def __rc(self):
    pass
  
  def __rw(self):
    pass
  
  def __uc(self):
    pass
  
  def __uw(self):
    pass
  
  def __lc(self):
    pass
  
  def __lwp(self):
    pass
  
  def __lwc(self):
    pass
  
  def __lwa(self):
    pass
  
  def __lwt(self):
    pass
  
  def __lw(self):
    pass

  # End Commands
  
  def run(self, cmd: str) -> int:
    if cmd == "fc":
      choice_list = self.__fc()
      print(self.__json_print.printCandidateComposerShort(choice_list))
      choice = self._processSelectedNumber(choice_list)
      print(self.__json_print.printComposerInfoLong(choice))
      
    elif cmd == "fw":
      choice_list = self.__fw()
      print(self.__json_print.printCandidateWorkShort(choice_list))
      choice = self._processSelectedNumber(choice_list)
      print(self.__json_print.printWorkInfoLong(choice))
      
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    elif cmd == "":
      pass
    else:
      pass

if __name__ == "__main__":
  default_dbpath = os.path.abspath('../../pytest/__dbtest')
  cmd = CommandLine(default_dbpath)
  cmd.run("fc")
  cmd.run("fw")