import sys, os, time, hashlib, string
import sanctus.constants as constants
from sanctus.db_base.dbutils import File_IO, TextTools

class Metadata_IO(File_IO, TextTools):
  def __init__(self, db_root=constants.DEFAULT_LOCAL_DB_DIR) -> None:
    super().__init__(db_root)
    self._METADATA_ROOT = "metadata/" 
    self._ARRANGEMENT_DIR = self._METADATA_ROOT + "arrangement/"
    self._COLLECTION_DIR = self._METADATA_ROOT + "collection/"
    self._PIECE_DIR = self._METADATA_ROOT + "piece/"
    self._TEMPLATE_DIR = self._METADATA_ROOT + "template/"
    if not self._checkDirectory():
      print("[WARNING] Metadata directory invalid")
      raise("Directory invalid")

  def _getRandomHash(self) -> str:
    m = hashlib.sha1()
    # get time for randomness
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
    m.update(str(t + str(time.time())).encode())
    return m.hexdigest()

  def _getAllMetadataJsonFileName(self) -> list:
    return list(string.digits + "abcdef")

  def _createPieceDict(self) -> dict:
    entry = {
      "DedicatedTo": "",
      "Title": "",
      "Subtitle": "",
      "Subsubtitle": "",
      "ComposerNameCode": "",
      "Type": "piece",
      "Year": "",
      "Opus": "",
      "Hash": ""
    }
    return entry
  
  def _createArrangementDict(self) -> dict:
    entry = {
      "DedicatedTo": "",
      "Title": "",
      "Subtitle": "",
      "Subsubtitle": "",
      "OrigInstrument": "",
      "ForInstrument": "",
      "ComposerNameCode": "",
      "Arranger": "",
      "Type": "arrangement",
      "Year": "",
      "Opus": "",
      "Hash": ""
    }
    return entry

  def _createTemplateDict(self) -> dict:
    entry = {
      "Title": "",
      "Instruments": [],
      "Type": "template",
      "Year": "",
      "Hash": ""
    }
    return entry

  def _createCollectionDict(self) -> dict:
    entry = {
      "DedicatedTo": "",
      "Title": "",
      "Subtitle": "",
      "Subsubtitle": "",
      "ComposerNameCode": "",
      "Type": "collection",
      "Opus": "",
      "Year": "",
      "Hash": "",
      "NumberOfPieces": "0",
      "PieceHash": []
    }
    return entry
  
  def _updateEntry(self, entry: dict, dkey: str, new_val='') -> dict:
    if dkey == "Type":
      raise("Cannot update protected key \"Type\"")
    elif dkey in entry.keys():
      entry[dkey] = new_val
    else:
      raise("Key \"{}\" not available".format(dkey))
    return entry

  def _updateEntryAddKey(self, entry: dict, dkey: str, new_val='') -> dict:
    if dkey == "Type":
      raise("Cannot update protected key \"Type\"")
    else:
      entry[dkey] = new_val
    return entry
  
  def _addUpdateEntry(self, entry: dict, dkey: str, new_val='') -> dict:
    if dkey == "Type":
      raise("Cannot update protected key \"Type\"")
    else:
      entry[dkey] = new_val
    return entry
  
  def _addWorkToCollection(self, entry: dict, new_work_hash: str) -> dict:
    if "Type" not in entry.keys():
      raise("Key \"Type\" not in dictionary")
      return entry
    if "PieceHash" not in entry.keys():
      raise("Key \"PieceHash\" not in dictionary")
      return entry
    
    if entry["Type"] != "collection":
      raise("Trying to add work to non collection.")
    else:
      entry["PieceHash"].append(new_work_hash)
    return entry

  def createItem(self, type_of_work: str, title='', subtitle='', subsubtitle='',
                 composercode='', opus='', instruments=[]) -> bool:
    try:
      item_hash = self._getRandomHash()
      first_letter = item_hash[0]
      entry = {}
      json_filename = ""

      if type_of_work.lower() == "piece":
        entry = self._createPieceDict()
        json_filename = self._PIECE_DIR + first_letter + self.JSON_EXTENTION
        
      elif type_of_work.lower() == "arrangement":
        entry = self._createArrangementDict()
        json_filename = self._ARRANGEMENT_DIR + first_letter + self.JSON_EXTENTION

      elif type_of_work.lower() == "collection":
        entry = self._createCollectionDict()
        json_filename = self._COLLECTION_DIR + first_letter + self.JSON_EXTENTION

      elif type_of_work.lower() == "template":
        entry = self._createTemplateDict()
        json_filename = self._TEMPLATE_DIR + first_letter + self.JSON_EXTENTION
      
      else:
        print("[INFO] Cannot create invalid type \"{}\"".format(type_of_work))
        entry = self._createPieceDict()
        return False
      
      entry = self._updateEntry(entry, dkey="Title", new_val=title)
      entry = self._updateEntry(entry, dkey="Subtitle", new_val=subtitle)
      entry = self._updateEntry(entry, dkey="Subsubtitle", new_val=subsubtitle)
      entry = self._updateEntry(entry, dkey="ComposerNameCode", new_val=composercode)
      entry = self._updateEntry(entry, dkey="Opus", new_val=opus)
      entry = self._updateEntry(entry, dkey="Hash", new_val=item_hash)
      entry = self._addUpdateEntry(entry, dkey="Instruments", new_val=instruments)

      if os.path.exists(json_filename):
        jsonobj = self.readJsonFileAsObj(json_filename)
        jsonobj.append(entry)
        self.writeJsonFile(jsonobj, json_filename + "~")
        self.fmoveReplace(json_filename + "~", json_filename)
      else:
        self.writeJsonFile([entry], json_filename)
      
      print("[INFO] Created {}: {}".format(type_of_work, item_hash))
      return True
    
    except RuntimeError as e:
      print("createItem(): Error: {}".format(e))
      return False
    except Exception as excp:
      print("createItem(): Exception: {}".format(excp))
      return False
    
    return False

  def deleteItem(self, hashcode='0') -> bool:
    first_letter = hashcode[0]
    filenames = [
      self._PIECE_DIR + first_letter + self.JSON_EXTENTION, 
      self._COLLECTION_DIR + first_letter + self.JSON_EXTENTION,
      self._ARRANGEMENT_DIR + first_letter + self.JSON_EXTENTION,
      self._TEMPLATE_DIR + first_letter + self.JSON_EXTENTION
    ]

    try:
      for name in filenames:
        if os.path.exists(name):
          entry = self.readJsonFileAsObj(name)
          # search hashcode in json file
          for item in entry:
            if item["Hash"] == hashcode:
              entry.remove(item)
          self.writeJsonFile(entry, name + "~")
          self.fmoveReplace(name + "~", name)
      return True
    
    except RuntimeError as e:
      print("deleteItem(): Error: {}".format(e))
      return False
    except Exception as excp:
      print("deleteItem(): Exception: {}".format(excp))
      return False
    
    return False

  def updateItem(self, hashcode='0', dkey='', new_val='', addkey=False) -> bool:
    first_letter = hashcode[0]
    filenames = [
      self._PIECE_DIR + first_letter + self.JSON_EXTENTION, 
      self._COLLECTION_DIR + first_letter + self.JSON_EXTENTION,
      self._ARRANGEMENT_DIR + first_letter + self.JSON_EXTENTION,
      self._TEMPLATE_DIR + first_letter + self.JSON_EXTENTION
    ]
    try:
      for name in filenames:
        if os.path.exists(name):
          entry = self.readJsonFileAsObj(name)
          new_item = {}
          # search hashcode in json file
          for item in entry:
            if item["Hash"] == hashcode:
              if addkey:
                new_item = self._updateEntryAddKey(item, dkey=dkey, new_val=new_val)
              else:
                new_item = self._updateEntry(item, dkey=dkey, new_val=new_val)
              entry.remove(item)
              entry.append(new_item)
          self.writeJsonFile(entry, name + "~")
          self.fmoveReplace(name + "~", name)
      return True

    except RuntimeError as e:
      print("deleteItem(): Error: {}".format(e))
    except Exception as excp:
      print("deleteItem(): Exception: {}".format(excp))
    
    return False

  def addWorkInCollection(self, coll_hashcode='0', new_work_hash='') -> bool:
    try:
      filename = self._COLLECTION_DIR + coll_hashcode[0] + self.JSON_EXTENTION
      if os.path.exists(filename):
        entry = self.readJsonFileAsObj(filename)
        for item in entry:
          if item["Hash"] == coll_hashcode:
            # get current list of work then update it
            list_work = item["PieceHash"]
            list_work.append(new_work_hash)
            new_item = self._updateEntry(item, dkey="PieceHash", new_val=list_work)
            # remove old item and append new item
            entry.remove(item)
            entry.append(new_item)
        
        self.writeJsonFile(entry, filename + "~")
        self.fmoveReplace(filename + "~", filename)
        return True

    except RuntimeError as e:
      print("addWorkInCollection(): Error: {}".format(e))
      return False
    except Exception as excp:
      print("addWorkInCollection(): Exception: {}".format(excp))
      return False
    
    return False

  def queryByTitle(self, title='') -> list:
    result = []
    try:
      for first_letter in self._getAllMetadataJsonFileName():
        # obtain list of possible filenames
        filenames = [
          self._PIECE_DIR + first_letter + self.JSON_EXTENTION, 
          self._COLLECTION_DIR + first_letter + self.JSON_EXTENTION,
          self._ARRANGEMENT_DIR + first_letter + self.JSON_EXTENTION,
          self._TEMPLATE_DIR + first_letter + self.JSON_EXTENTION
        ]
        for fn in filenames:
          if os.path.exists(fn):
            jsonobj = self.readJsonFileAsObj(fn)
            for item in jsonobj:
              # make sure key is in dict
              if "Title" in item.keys() and "Subtitle" in item.keys() \
                and "Subsubtitle" in item.keys():
                # lower case search in title; subtitle and subsubtitle
                if title.lower() in item["Title"].lower() \
                  or title.lower() in item["Subtitle"].lower() \
                  or title.lower() in item["Subsubtitle"].lower():
                  result.append(item)
      return result

    except RuntimeError as e:
      print("queryByTitle(): Error: {}".format(e))
      return result
    except Exception as excp:
      print("queryByTitle(): Exception: {}".format(excp))
      return result

  def queryByYear(self, year='') -> list:
    result = []
    try:
      for first_letter in self._getAllMetadataJsonFileName():
        # obtain list of possible filenames
        filenames = [
          self._PIECE_DIR + first_letter + self.JSON_EXTENTION, 
          self._COLLECTION_DIR + first_letter + self.JSON_EXTENTION,
          self._ARRANGEMENT_DIR + first_letter + self.JSON_EXTENTION,
          self._TEMPLATE_DIR + first_letter + self.JSON_EXTENTION
        ]
        for fn in filenames:
          if os.path.exists(fn):
            jsonobj = self.readJsonFileAsObj(fn)
            for item in jsonobj:
              if "Year" in item.keys():
                if year == item["Year"].lower():
                  result.append(item)
      return result

    except RuntimeError as e:
      print("queryByYear(): Error: {}".format(e))
      return result
    except Exception as excp:
      print("queryByYear(): Exception: {}".format(excp))
      return result

  def queryByOpus(self, opus='') -> list:
    result = []
    
    try:
      for first_letter in self._getAllMetadataJsonFileName():
        # obtain list of possible filenames
        filenames = [
          self._PIECE_DIR + first_letter + self.JSON_EXTENTION, 
          self._COLLECTION_DIR + first_letter + self.JSON_EXTENTION,
          self._ARRANGEMENT_DIR + first_letter + self.JSON_EXTENTION,
          self._TEMPLATE_DIR + first_letter + self.JSON_EXTENTION
        ]
        for fn in filenames:
          if os.path.exists(fn):
            jsonobj = self.readJsonFileAsObj(fn)
            for item in jsonobj:
              if "Opus" in item.keys():
                # preprocess opus system and opus number
                opus_query = opus.lower().replace(".","").replace(" ","").replace("opus","op")
                opus_target = item["Opus"].lower().replace(".","").replace(" ","").replace("opus","op")
                if opus_query in opus_target:
                  result.append(item)
      return result

    except RuntimeError as e:
      print("queryByOpus(): Error: {}".format(e))
      return result
    except Exception as excp:
      print("queryByOpus(): Exception: {}".format(excp))
      return result

  def queryByComposerCode(self, name_code='') -> list:
    result = []
    
    try:
      for first_letter in self._getAllMetadataJsonFileName():
        # obtain list of possible filenames
        filenames = [
          self._PIECE_DIR + first_letter + self.JSON_EXTENTION, 
          self._COLLECTION_DIR + first_letter + self.JSON_EXTENTION,
          self._ARRANGEMENT_DIR + first_letter + self.JSON_EXTENTION,
          self._TEMPLATE_DIR + first_letter + self.JSON_EXTENTION
        ]
        for fn in filenames:
          if os.path.exists(fn):
            jsonobj = self.readJsonFileAsObj(fn)
            for item in jsonobj:
              if "ComposerNameCode" in item.keys():
                if name_code == item["ComposerNameCode"]:
                  result.append(item)
      return result

    except RuntimeError as e:
      print("queryByComposerCode(): Error: {}".format(e))
      return result
    except Exception as excp:
      print("queryByComposerCode(): Exception: {}".format(excp))
      return result

  def queryByType(self, type_of_work='piece') -> list:
    result = []
    filename = ""
    try:
      for first_letter in self._getAllMetadataJsonFileName():
        # get filename based on the input
        if type_of_work.lower() == "piece":
          filename = self._PIECE_DIR + first_letter + self.JSON_EXTENTION
        elif type_of_work.lower() == "collection":
          filename = self._COLLECTION_DIR + first_letter + self.JSON_EXTENTION
        elif type_of_work.lower() == "template":
          filename = self._TEMPLATE_DIR + first_letter + self.JSON_EXTENTION
        elif type_of_work.lower() == "arrangement":
          filename = self._ARRANGEMENT_DIR + first_letter + self.JSON_EXTENTION
        else:
          filename = "unknown" + self.JSON_EXTENTION

        if os.path.exists(filename):
          jsonobj = self.readJsonFileAsObj(filename)
          for item in jsonobj:
            if "Type" in item.keys():
              if type_of_work.lower() == item["Type"].lower():
                result.append(item)
      return result

    except RuntimeError as e:
      print("queryByType(): Error: {}".format(e))
      return result
    except Exception as excp:
      print("queryByType(): Exception: {}".format(excp))
      return result