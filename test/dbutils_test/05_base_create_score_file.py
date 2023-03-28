import os, sys
sys.path.append('../..')
sys.path.append('..')
import setup_test

from sanctus.db_base.db_score import Score_IO
from sanctus.db_base.db_metadata import Metadata_IO

"""
Testing db_base/db_score.py base class
"""

# Connect to DB
mio = Metadata_IO(setup_test.db_abs_path)
sio = Score_IO(setup_test.db_abs_path)

op13_hashcode = mio.queryByOpus("op13")[0]["Hash"]

# create 15 empty files
for i in range(15):
  sio.createEngravingFile(op13_hashcode)
