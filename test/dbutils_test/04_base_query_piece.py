import os, sys
sys.path.append('../..')
sys.path.append('..')
import setup_test

from sanctus.db_base.db_composer import Composer_IO
from sanctus.db_base.db_metadata import Metadata_IO

"""
Testing db_base/db_metadata.py base class
"""

# Connect to DB
cio = Composer_IO(setup_test.db_abs_path)
mio = Metadata_IO(setup_test.db_abs_path)

print("")
print("queryByTitle - \"Prelude\":")
print(mio.queryByTitle("prelude"))

print("")
print("queryByTitle - \"Sonata\":")
print(mio.queryByTitle("sonata"))

print("")
print("queryByOpus - \"Op. 13\":")
print(mio.queryByOpus("op13"))

print("")
print("queryByComposerCode - \"frescobaldi\":")
print(mio.queryByComposerCode("F-g_a_frescobaldi"))

op13 = mio.queryByOpus("op13")
print("")
print("queryByHash - using Beethoven op13 hash:")
print(mio.queryByHash(op13[0]["Hash"]))
print("")