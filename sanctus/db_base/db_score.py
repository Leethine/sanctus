import os, sys, tarfile, base64
import sanctus.constants as constants
from sanctus.db_base.dbutils import File_IO, TextTools

class Score_IO(File_IO, TextTools):
  def __init__(self, db_root=constants.DEFAULT_DB_DIR_PATH) -> None:
    super().__init__(db_root)
    self._SCORE_ROOT = "score/" 
    self._FILE_DIR = self._SCORE_ROOT
    self._TARFILE_EXTENTION = ".tar.gz"
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
  
  def getScoreDirAbs(self, hashcode: str) -> str:
    if self.getScoreDir(hashcode):
      return os.path.abspath(self.getScoreDir(hashcode))
    else:
      return ''

  def getListOfScript(self, hashcode: str, extension='.ly') -> list:
    score_dir = self.getScoreDirAbs(hashcode)
    scorefiles = []
    if not score_dir:
      return []
    elif score_dir:
      scorefiles = [f for f in os.listdir(score_dir) if os.path.isfile(os.path.join(score_dir, f))]
    else:
      print("[WARNING] Hash conflict: {}".format(hashcode))
      return []
    
    # filter, only get ".ly" files
    scorefiles = [f for f in scorefiles if extension in f]
    return scorefiles

  def createEngravingFile(self, hashcode: str, extension='.ly', content='% ---- ') -> bool:
    score_dir = self.getScoreDirAbs(hashcode)

    # dir doesn't exist, create dir and file
    if not score_dir and hashcode != "":
      score_dir = self._FILE_DIR + hashcode[0] + "/" + hashcode
      os.mkdir(score_dir)
      with open(score_dir + "/" + "01" + extension, "w") as f:
        f.write(content)
      print("[INFO] Empty engraving file created with hash {}".format(hashcode))
      return True
    else:    
      # dir path exists, create file directly
      if os.path.exists(score_dir) and hashcode != "":
        score_list = self.getListOfScript(hashcode)
        if not score_list:
          # if no score exists in directory, create new file
          with open(score_dir + "/" + "01" + extension, "w") as f:
            f.write(content)
          print("[INFO] Empty engraving file created with hash {}".format(hashcode))
          return True
        else:
          # if score already exist in directory, create next file
          score_list = [fn.replace(".ly", "") for fn in score_list]
          score_list.sort()
          next_file = int(score_list[-1]) + 1
          next_file = "{:0>2d}".format(next_file)
          with open(score_dir + "/" + next_file + extension, "w") as f:
            f.write(content)
          print("[INFO] Empty engraving file created with hash {}".format(hashcode))
          return True
      return False
    
    return False
  
  def packScoreDir(self, hashcode: str, extension='.ly') -> str:
    scorepath = self.getScoreDirAbs(hashcode)
    if not scorepath:
      return ''
    else:
      tarpath = scorepath + "/" + hashcode + self._TARFILE_EXTENTION
      if os.path.exists(tarpath):
        os.remove(tarpath)
      with tarfile.open(tarpath, mode='x:gz') as tar:
        for fname in self.getListOfScript(hashcode, extension):
          tar.add(scorepath + "/" + fname)
      return tarpath
  
  def getScorePackageAsRaw(self, hashcode: str, extension='.ly') -> bytes:
    scorepath = self.getScoreDirAbs(hashcode)
    tarpath = scorepath + "/" + hashcode + self._TARFILE_EXTENTION
    if os.path.exists(tarpath):
      with open(tarpath, "rb") as tar:
        return base64.b64encode(tar.read())
    else:
      return b""

  def unpackScoreDir(self, hashcode: str, extension='.ly') -> bool:
    scorepath = self.getScoreDirAbs(hashcode)
    tarpath = scorepath + "/" + hashcode + self._TARFILE_EXTENTION
    if not os.path.exists(tarpath):
      print("[Warning] <unpackScoreDir> tarball does not exist")
      return False
    else:
      for fname in self.getListOfScript(hashcode, extension):
        os.remove(scorepath + "/" + fname)
      with tarfile.open(tarpath, mode='r:gz') as tar:
        for member in tar.getmembers():
          if member.isreg():
            member.name = os.path.basename(member.name)
            tar.extract(member, path=scorepath)
        print("[INFO] Extracted {} files".format(len(tar.getmembers())))
      return True

