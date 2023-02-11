import os

from db_base.db_composer import Composer_IO
from db_base.db_metadata import Metadata_IO
from db_base.db_score import Score_IO

"""
add composer
add piece
add collection
add arrangement
add template

find composer by abbrname ABBRNAME

find/open/new piece by title TITLE
find/open/new arrangement by title TITLE
find/open collection by title TITLE

find/open/new piece by opus OPUS
find/open/new arrangement by opus OPUS
find/open collection by opus OPUS

find/open/new piece by composer ABBRNAME
find/open/new arrangement by composer ABBRNAME
find/open collection by composer ABBRNAME
"""

class CommandLine():
  def __init__(self, dbpath='~/') -> None:
    self.__c = Composer_IO(dbpath)
    self.__m = Metadata_IO(dbpath)
    self.__s = Score_IO(dbpath)
  
  def _processSelectedNumber(self, num: int) -> dict:
    pass

  def run(self) -> int:
    pass

if __name__ == "__main__":
  default_dbpath = os.path.abspath('~/Music/sanctus_db/data_v1')
  cmd = CommandLine(default_dbpath)
  cmd.run()