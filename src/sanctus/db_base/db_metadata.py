import os, json
import constants
from dbutils import File_IO, TextTools

class Metadata_IO(File_IO, TextTools):
  def __init__(self, db_root=constants.DEFAULT_LOCAL_DB_DIR) -> None:
    super().__init__(db_root)
    self.ARRANGEMENT_DIR = "arrangement/"
    self.COLLECTION_DIR = "collection/"
    self.PIECE_DIR = "piece/"
    self.TEMPLATE_DIR = "template/"
    self.ACTIVATED = False

  def activate(self) -> None:
    self._chdirToMetadataDir()
    self.ACTIVATED = True
  
  def deactivate(self) -> None:
    if self.ACTIVATED:
      os.chdir('..')
      self.ACTIVATED = False
    else:
      pass

  def _checkDirectory(self) -> bool:
    if self.getCWD() == os.path.abspath(os.path.curdir):
      return True
    else:
      return False
  
  def _chdirToMetadataDir(self) -> None:
    try:
      if self._checkDirectory():
        os.chdir("metadata")
      else:
        raise Exception("_chdirToMetadataDir(): Error: " + self.DB_ROOT)
    except RuntimeError as e:
      print("_chdirToMetadataDir(): runtime error {}".format(e))
    except Exception as excp:
      print(excp)

