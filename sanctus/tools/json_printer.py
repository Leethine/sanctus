import json

class JsonPrinter:
  def __init__(self) -> None:
    pass
  
  def _checkKeys(self, jobj:dict, lkey: list) -> bool:
    for k in lkey:
      if not k in jobj.keys():
        return False
    return True
  
  def _getKeyValue(self, jobj:dict, dkey='') -> str:
    if dkey in jobj.keys():
      return jobj[dkey]
    else:
      return ""
  
  def printComposerInfoShort(self, jobj: dict) -> str:
    list_keys = ["GivenNameList", "FamilyNameParticle", "FamilyNameList", "Born", "Died"]
    msgStr = ""
    
    if not self._checkKeys(jobj, list_keys):
      return ""
    
    try:
      # take initials of given name
      for n in self._getKeyValue(jobj, "GivenNameList"):
        msgStr += n[0] + "."
      
      # take family name
      msgStr += "\t" + self._getKeyValue(jobj, "FamilyNameList")[0]
      
      # take birth and death year
      msgStr += "\t" + "(" + self._getKeyValue(jobj, "Born") + "-" + self._getKeyValue(jobj, "Died") + ")"
      
      return msgStr
    except:
      print("[Error] <printComposerInfoShort> Invalid composer dict: ")
      print(jobj)
      return ""
  
  def printCandidateComposerShort(self, jobj: list) -> str:
    index = 1
    msgStr = ""
    for item in jobj:
      msgStr += str(index) + ")\t" + self.printComposerInfoShort(item) + "\n"
      index += 1
    return msgStr
  
  def printComposerInfoLong(self, jobj: dict) -> str:
    msgStr = ""
    try:
      msgStr += "Name:\t"            
      msgStr += "-".join(self._getKeyValue(jobj, "GivenNameList"))
      msgStr += " " + self._getKeyValue(jobj, "FamilyNameParticle") + " "
      msgStr += "-".join(self._getKeyValue(jobj, "FamilyNameList"))
      msgStr += " " + self._getKeyValue(jobj, "NamePostfix")

      msgStr += "\nComposer code:\t"
      msgStr += self._getKeyValue(jobj, "NameCode")

      msgStr += "\nYear:\t"
      msgStr += "(" + self._getKeyValue(jobj, "Born") + " - " + self._getKeyValue(jobj, "Died") + ")"
      
      msgStr += "\nStyle:\t"
      msgStr += ",".join(self._getKeyValue(jobj, "Style"))
      
      msgStr += "\nWikipedia link:\t"
      msgStr += self._getKeyValue(jobj, "wikiLink")
      
      msgStr += "\nIMSLP link:\t"
      msgStr += self._getKeyValue(jobj, "imslpLink")
      
      return msgStr
    except:
      print("[Error] <printComposerInfoLong> Invalid composer dict: ")
      print(jobj)
      return ""
  
  def printWorkInfoShort(self, jobj: dict) -> str:
    list_keys = ["Title", "ComposerNameCode", "Type", "Opus"]
    msgStr = ""
    
    if not self._checkKeys(jobj, list_keys):
      return ""
    
    try:
      msgStr += "Title:\t"
      msgStr += self._getKeyValue(jobj, "Title")
      
      msgStr += "\nComposerCode:\t"
      msgStr += self._getKeyValue(jobj, "ComposerNameCode")
      
      msgStr += "\nType:\t"
      msgStr += self._getKeyValue(jobj, "Type")
      
      msgStr += "\tOpus:\t"
      msgStr += self._getKeyValue(jobj, "Opus")
      
      return msgStr
    except:
      print("[Error] <printWorkInfoShort> Invalid work info dict: ")
      print(jobj)
      return ""

  def printCandidateWorkShort(self, jobj: list) -> str:
    index = 1
    msgStr = ""
    for item in jobj:
      msgStr +=  "[" + str(index) + "]"
      msgStr += "\n" + self.printWorkInfoShort(item) + "\n"
      index += 1
    return msgStr

  def printWorkInfoLong(self, jobj: dict) -> str:
    list_keys = ["Title", "Subtitle", "Subsubtitle", "ComposerNameCode", "Type", "Opus", "Instruments"]
    msgStr = ""
    
    if not self._checkKeys(jobj, list_keys):
      return ""
    
    try:
      msgStr += "Title:\t"
      msgStr += self._getKeyValue(jobj, "Title")
      msgStr += "\nSubitle:\t"
      msgStr += self._getKeyValue(jobj, "Subitle")
      msgStr += "\nSubsubitle:\t"
      msgStr += self._getKeyValue(jobj, "Subsubitle")
      
      msgStr += "\nComposerCode:\t"
      msgStr += self._getKeyValue(jobj, "ComposerNameCode")
      
      msgStr += "\nType:\t"
      msgStr += self._getKeyValue(jobj, "Type")
      
      msgStr += "\tOpus:\t"
      msgStr += self._getKeyValue(jobj, "Opus")
      
      msgStr += "\nFor instruments:\n"
      for instrument in self._getKeyValue(jobj, "Instruments"):
        msgStr += "\t" + instrument + "\n"
      
      return msgStr
    except:
      print("[Error] <printWorkInfoLong> Invalid work info dict: ")
      print(jobj)
      return ""