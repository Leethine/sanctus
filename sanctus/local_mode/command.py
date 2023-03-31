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
  
  def __MACRO_input(self, prompt: str) -> str:
    return input(prompt)
  
  def __MACRO_print(self, message: str) -> None:
    print(message)
  
  def processInput(self, prompt: str) -> str:
    input_str = self.__MACRO_input(prompt)
    input_str = re.sub('[^a-zA-Z0-9_\.\s\-]', '', input_str)
    return input_str
  
  def _processSelectedNumber(self, candidates: list) -> dict:
    try:
      if not candidates:
        return {}
      elif len(candidates) == 1:
        return candidates[0]
      else:
        while True:
          selected = self.__MACRO_input("> Select an item [1-"+str(len(candidates))+"]: ")
          selected = int(re.sub('\D', '', selected)) - 1
          if selected < len(candidates) and selected >= 0:
            return candidates[selected]
          else:
            self.__MACRO_print(str(selected) + " is out of range, please select again!")
    except:
      print("[Error] <_processSelectedNumber> cannot process")
      return {}
  
  ################# Begin Commands #################
  def _fc(self) -> dict:
    choice_list = []
    search_str = self.processInput("> Find composer: ")
    if "." in search_str:
      choice_list = self.__cli.findComposer("abbr", search_name=search_str)
    elif "1" in search_str or "2" in search_str:
      choice_list = self.__cli.findComposer("year", search_name=search_str)
    else:
      # note: disable full name search
      choice_list = self.__cli.findComposer("fmlyname", search_name=search_str) \
            + self.__cli.findComposer("abbr", search_name=search_str)
    
    if choice_list:
      self.__MACRO_print(self.__json_print.printCandidateComposerShort(choice_list))
      choice = self._processSelectedNumber(choice_list)
      self.__MACRO_print(self.__json_print.printComposerInfoLong(choice))
      return choice
    else:
      self.__MACRO_print("Composer not found.")
      return {}
  
  def _fw_all(self) -> list:
    search = self.processInput("> Find work: ")
    
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
      #self.__MACRO_print(by_composer)
      return self.__cli.findWork(find_by='fname', search_string=search)

    # in the end, try finding by title
    found = self.__cli.findWork(find_by='title', search_string=search)
    if found:
      return found
    
    return []
    
  def _fw_p(self) -> list:
    found = self._fw_all()
    result = []
    if found:
      for item in found:
        if item["Type"] == "piece":
          result.append(item)
    return result
  
  def _fw_c(self) -> list:
    found = self._fw_all()
    result = []
    if found:
      for item in found:
        if item["Type"] == "collection":
          result.append(item)
    return result
  
  def _fw_a(self) -> list:
    found = self._fw_all()
    result = []
    if found:
      for item in found:
        if item["Type"] == "arrangement":
          result.append(item)
    return result
  
  def _fw_t(self) -> list:
    found = self._fw_all()
    result = []
    if found:
      for item in found:
        if item["Type"] == "template":
          result.append(item)
    return result

  def _fw(self, cmd: str) -> dict:
    if "fw" == cmd[0:2]:
      choice_list = []
      if cmd == "fwp":
        choice_list = self._fw_p()
      elif cmd == "fwc":
        choice_list = self._fw_c()
      elif cmd == "fwa":
        choice_list = self._fw_a()
      elif cmd == "fwt":
        choice_list = self._fw_t()
      elif cmd == "fw":
        choice_list = self._fw_all()
      else:
        self.__MACRO_print("[WARNING] Bad command")
        return {}
      
      self.__MACRO_print(self.__json_print.printCandidateWorkShort(choice_list))
      choice = self._processSelectedNumber(choice_list)
      self.__MACRO_print(self.__json_print.printWorkInfoLong(choice))
      return choice
    else:
      self.__MACRO_print("[WARNING] Bad command")
      return {}
  
  def _nc(self) -> None:
    self.__MACRO_print("Creating new composer...\n")
    try:
      confirm_msg = ""
      fml_name = self.processInput("> Family Name: ").split(' ')
      confirm_msg += "FamilyName: " + '-'.join(fml_name) + "\n"
      
      potential_existed = self.__cli.findComposer(find_by="fmlyname", search_name=fml_name[0])
      if potential_existed:
        self.__MACRO_print("\n[INFO] The composer you are creating may exist:")
        for item in potential_existed:
          self.__MACRO_print(self.__json_print.printComposerInfoShort(item))
        
        if self.processInput("Still create? [Y/n] ").capitalize() != "Y":
          self.__MACRO_print("[INFO] Composer creation abandoned.")
          return None

      gvn_name = self.processInput("> Given Name: ").split(' ')
      confirm_msg += "GivenName: " + '-'.join(gvn_name) + "\n"
      
      b_year = self.processInput("> Born Year: ")
      confirm_msg += "Born: " + b_year + "\n"
      
      d_year = self.processInput("> Died Year: ")
      confirm_msg += "Died: " + d_year + "\n"
      
      known_name = self.processInput("> Known Name: ")
      confirm_msg += "Known as: " + known_name + "\n"
      
      styles = self.processInput("> List of styles (separate by space):\n> ").split(' ')
      confirm_msg += "Style: " + ','.join(styles) + "\n"
      
      wiki = ""
      confirm = "n"
      while not (confirm == "y" or confirm == "Y"):
        wiki = self.__MACRO_input("\n> Wikipedia link:\n> ")
        self.__MACRO_print("\nYour input is:\n" + wiki)
        confirm = self.processInput("Confirm? [Y/n] ")
      confirm_msg += "Wikipedia: " + wiki + "\n"
      
      imslp = ""
      confirm = "n"
      while not (confirm == "y" or confirm == "Y"):
        imslp = self.__MACRO_input("\n> IMSLP link:\n> ")
        self.__MACRO_print("\nYour input is:\n" + imslp)
        confirm = self.processInput("Confirm? [Y/n] ")
      confirm_msg += "IMSLP: " + imslp + "\n"
      
      confirm = "n"
      self.__MACRO_print("\n----------------------------")
      self.__MACRO_print("|  Composer to be created  |")
      self.__MACRO_print("----------------------------")
      self.__MACRO_print(confirm_msg)
      confirm = self.processInput("Confirm? [Y/n] ")
      self.__MACRO_print("\n")
      
      if confirm == "y" or confirm == "Y":
        if self.__cli.addComposer(given_name_list=gvn_name,
                                  family_name_list=fml_name,
                                  born_year=b_year, died_year=d_year,
                                  known_as_name=known_name, style=styles,
                                  wiki_link=wiki, imslp_link=imslp):
          self.__MACRO_print("[INFO] Composer created: ")
          self.__MACRO_print(confirm_msg)
        else:
          self.__MACRO_print("[INFO] Composer failed!")
        return None
      else:
        self.__MACRO_print("[INFO] Composer creation abandoned.")
        return None
    except:
      self.__MACRO_print("[WARNING] Composer creation stopped!")
      self.__MACRO_print(confirm_msg)
      return None
  
  def _nw(self, work_type='') -> None:
    # process composer first
    self.__MACRO_print("Who is the composer of the work?")
    composer = self._fc()
    if not composer:
      self.__MACRO_print("Composer does not exist, consider creating the entry.")
      return None
    
    if not work_type:
      wt = self.processInput("> Choose the work type (p/a/c/t): ") 
      temp_dict = {"p": "piece", "c": "collection", "t": "template", "a": "arrangement"}
      while True:
        if wt == "abd" or wt == "abandon":
          return None
        elif wt in temp_dict.keys():
          work_type = temp_dict[wt]
          break
        else:
          wt = self.processInput("Invalid choice!\nChoose the work type: >\n[p/a/c/t] (abd for abandon)")
    
    if "NameCode" in composer.keys():
      title = self.processInput("> Title: ")
      subtitle = self.processInput("> Subtitle: ")
      subsubtitle = self.processInput("> Subsubtitle: ")
      ops = self.processInput("> Opus: ")
      instruments = self.processInput("> Instruments: ").split(" ")
      
      confirm = self.processInput("> Confirm creation? [y/n]")
      
      if confirm == "y":
        if self.__cli.addWork(type_of_work=work_type,
                          title=title,
                          subtitle=subtitle,
                          subsubtitle=subsubtitle,
                          composer_name_code=composer["NameCode"],
                          opus=ops,
                          instrument_list=instruments):
          self.__MACRO_print("[INFO] Created work: \"{}\"".format(title))
        else:
          self.__MACRO_print("[INFO] Failed to create: \"{}\"".format(title))          
      else:
        self.__MACRO_print("[INFO] Action abandoned.")
    else:
      self.__MACRO_print("[INFO] Data is broken. No action.")
    return None

  def _apc(self) -> None:
    self.__MACRO_print("Which piece/arrangement?")
    piece = self._fw("fwp")
    if not piece:
      self.__MACRO_print("Not Found.")
      return None
    
    self.__MACRO_print("Add this piece to which collection?")
    collection = self._fw("fwc")
    if not collection:
      self.__MACRO_print("Not Found.")
      return None
    
    self.__cli.addPieceToCollection(collection["Hash"], piece["Hash"])
    self.__MACRO_print("[INFO] Added {} to {}".format(piece["Title"], collection["Title"]))
    
  def _rc(self) -> None:
    self.__MACRO_print("Which composer to remove from DB?")
    composer = self._fc()
    if composer:
      if self.__cli.deleteComposer(composer["NameCode"]):
        self.__MACRO_print("[INFO] Removed composer: {}".format(composer["NameCode"]))
      else:
        self.__MACRO_print("[INFO] Not removed: {}".format(composer["NameCode"]))
    else:
      self.__MACRO_print("Not Found")
  
  def _rw(self) -> None:
    self.__MACRO_print("Which work to remove from DB?")
    work = self._fw("fw")
    if work:
      if self._cli.deleteWork(work["HashCode"]):
        self.__MACRO_print("[INFO] Removed work: {} - {}".format(work["Title"], work["Opus"]))
      else:
        self.__MACRO_print("[INFO] Not removed: {} - {}".format(work["Title"], work["Opus"]))
    else:
      self.__MACRO_print("Not Found")
  
  def _lc(self) -> list:
    ls = self.__cli.lsComposer()
    self.__MACRO_print("Initial\tFamilyName\tYear")
    for item in ls:
      self.__MACRO_print(self.__json_print.printComposerInfoShort(item))
    return ls
  
  def _lwp(self) -> list:
    ls = self.__cli.lsWork(worktype="piece")
    self.__MACRO_print("--------------------------------")
    for item in ls:
      self.__MACRO_print(self.__json_print.printWorkInfoShort(item))
      self.__MACRO_print("--------------------------------")
    return ls
  
  def _lwc(self) -> list:
    ls = self.__cli.lsWork(worktype="collection")
    self.__MACRO_print("--------------------------------")
    for item in ls:
      self.__MACRO_print(self.__json_print.printWorkInfoShort(item))
      self.__MACRO_print("--------------------------------")
    return ls
  
  def _lwa(self) -> list:
    ls = self.__cli.lsWork(worktype="arrangement")
    self.__MACRO_print("--------------------------------")
    for item in ls:
      self.__MACRO_print(self.__json_print.printWorkInfoShort(item))
      self.__MACRO_print("--------------------------------")
    return ls
  
  def _lwt(self) -> list:
    ls = self.__cli.lsWork(worktype="template")
    self.__MACRO_print("--------------------------------")
    for item in ls:
      self.__MACRO_print(self.__json_print.printWorkInfoShort(item))
      self.__MACRO_print("--------------------------------")
    return ls

  def _lw(self) -> list:
    ls = self.__cli.lsWork(worktype="all")
    self.__MACRO_print("--------------------------------")
    for item in ls:
      self.__MACRO_print(self.__json_print.printWorkInfoShort(item))
      self.__MACRO_print("--------------------------------")
    return ls

  def _uc(self) -> dict:
    pass
  
  def _uw(self) -> dict:
    pass

  ################# End Commands #################
  
  def run_cmd(self, cmd: str) -> None:
    if cmd == "fc":
      self._fc()
    elif "fw" == cmd[0:2]:
      self._fw(cmd)
    elif cmd == "nc":
      self._nc()
    elif cmd == "nw":
      self._nw()
    elif cmd == "apc":
      self._apc()
    elif cmd == "rc":
      self._rc()
    elif cmd == "rw":
      self._rw()
    elif cmd == "lc":
      self._lc()
    elif cmd == "lw":
      self._lw()
    elif cmd == "lwp":
      self._lwp()
    elif cmd == "lwa":
      self._lwa()
    elif cmd == "lwc":
      self._lwc()
    elif cmd == "lwt":
      self._lwt()
    else:
      self.__MACRO_print("[INRO] Invalid command, nothing to do.")
  
  def run(self) -> None:
    while True:
      cmd = self.processInput(">> ")
      if cmd.lower() == "exit":
        break
      elif cmd.lower() == "quit":
        break
      else:
        self.run_cmd(cmd)

