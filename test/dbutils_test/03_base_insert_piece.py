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

# Insert score metadata in DB
mio.createItem("piece", title="Piano Sonata No.8", composercode="B-l_van_beethoven", opus="Op. 13", instruments=["Piano"])
mio.createItem("piece", title="Prelude and Fugue in C minor", composercode="B-j_s_bach", opus="BWV 847", instruments=["Klavier","Harpsichord","Piano","Organ"])
mio.createItem("collection", title="15 Inventions", composercode="B-j_s_bach", opus="BWV 772-786", instruments=["Klavier","Harpsichord","Piano","Organ"])
mio.createItem("collection", title="Fiori Musicali", composercode="F-g_a_frescobaldi", opus="F. 12", instruments=["Organ"])