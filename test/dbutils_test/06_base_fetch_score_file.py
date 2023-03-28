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
print("Score is stored in:")
print(sio.getScoreDirAbs(op13_hashcode))

print(sio.packScoreDir(op13_hashcode))

sio.unpackScoreDir(op13_hashcode)

rawtar = sio.getScorePackageAsRaw(op13_hashcode)
sio.uploadScorePackageAsRaw(op13_hashcode, rawtar)
sio.unpackScoreDir(op13_hashcode)