import os
import constants
from db_base.dbutils import File_IO, TextTools

class Score_IO(File_IO, TextTools):
  def __init__(self, db_root=constants.DEFAULT_LOCAL_DB_DIR) -> None:
    super().__init__(db_root)
    self._SCORE_ROOT = "score/" 
    self._FILE_DIR = self._SCORE_ROOT + "file/"
    self._TEMPLATE_DIR = self._SCORE_ROOT + "template/"
    if not self._checkDirectory():
      print("[WARNING] Composer directory invalid")
      raise("Directory invalid")

  def getScoreDir(self, hashcode: str) -> str:
    if hashcode != "":
      first_letter = hashcode[0]
      score_dir = self._FILE_DIR + str(first_letter) + "/" + hashcode
      if os.path.exists(score_dir):
        return score_dir
      else:
        return ''
    else:
      return ''

  def getTemplateDir(self, hashcode: str) -> str:
    if hashcode != "":
      first_letter = hashcode[0]
      template_dir = self._TEMPLATE_DIR + str(first_letter) + "/" + hashcode
      if os.path.exists(template_dir):
        return template_dir
      else:
        return ''
    else:
      return ''
  
  def getScoreDirAbs(self, hashcode: str) -> str:
    if self.getScoreDir(hashcode):
      return os.path.abspath(self.getScoreDir(hashcode))
    else:
      return ''

  def getTemplateDirAbs(self, hashcode: str) -> str:
    if self.getTemplateDir(hashcode):
      return os.path.abspath(self.getTemplateDir(hashcode))
    else:
      return ''

  def getListOfScript(self, hashcode: str, extension=".ly") -> list:
    score_dir = self.getScoreDirAbs(hashcode)
    template_dir = self.getTemplateDirAbs(hashcode)
    scorefiles = []
    if not score_dir and not template_dir:
      return []
    elif not score_dir and template_dir:
      scorefiles = [f for f in os.listdir(template_dir) if os.path.isfile(os.path.join(template_dir, f))]
    elif score_dir and not template_dir:
      scorefiles = [f for f in os.listdir(score_dir) if os.path.isfile(os.path.join(score_dir, f))]
    else:
      print("[WARNING] Hash conflict: {}".format(hashcode))
      return []
    
    # filter, only get ".ly" files
    scorefiles = [f for f in scorefiles if extension in f]
    return scorefiles

  def createNewEngravingFile(self, hashcode: str, filetype='score', extension='.ly') -> bool:
    score_dir = ""
    if filetype.lower() == "score":
      score_dir = self.getScoreDirAbs(hashcode)
    elif filetype.lower() == "template":
      score_dir = self.getTemplateDirAbs(hashcode)
    else:
      return False

    # dir doesn't exist, create dir and file
    if not score_dir and hashcode != "":
      if filetype.lower() == "score":
        score_dir = self._FILE_DIR + hashcode[0] + "/" + hashcode
        os.mkdir(score_dir)
        with open(score_dir + "/" + "01" + extension, "w") as f:
          f.write("%!: ---- ")
        print("[INFO] New engraving file created with hash = {}".format(hashcode))
        return True
      elif filetype.lower() == "template":
        score_dir = self._TEMPLATE_DIR + hashcode[0] + "/" + hashcode
        os.mkdir(score_dir)
        with open(score_dir + "/" + "01" + extension, "w") as f:
          f.write("%!: ---- ")
        print("[INFO] New engraving file created with hash = {}".format(hashcode))
        return True
      else:
        return False

    if os.path.exists(score_dir) and hashcode != "":
      score_list = self.getListOfScript(hashcode)
      if not score_list:
        # if no score exists in directory, create new file
        with open(score_dir + "/" + "01" + extension, "w") as f:
          f.write("%!: ---- ")
        print("[INFO] New engraving file created with hash = {}".format(hashcode))
        return True
      else:
        # if score already exist in directory, create next file
        score_list = [fn.replace(".ly", "") for fn in score_list]
        score_list.sort()
        next_file = int(score_list[-1]) + 1
        next_file = "{:0>2d}".format(next_file)
        with open(score_dir + "/" + next_file + extension, "w") as f:
          f.write("%!: ---- ")
        print("[INFO] New engraving file created with hash = {}".format(hashcode))
        return True
    
    return False
