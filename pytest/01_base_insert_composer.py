import os, sys
sys.path.append('..')
import setup_test

from sanctus.db_base.db_composer import Composer_IO

"""
Testing db_base/db_composer.py base class
Insertion
"""

# Connect to DB
cio = Composer_IO(setup_test.db_abs_path)

# Insert composers in DB
cio.createComposerEntry(["Girolamo", "Alessandro"], ["Frescobaldi"], "1583", "1643", style=["Renaissance", "Early Baroque"])
cio.createComposerEntry(["George", "Frideric"], ["Handel"], "1685", "1759", style=["Baroque"])
cio.createComposerEntry(["Johann", "Sebastian"], ["Bach"], "1685", "1750", style=["Baroque"])
cio.createComposerEntry(["Wolfgang", "Amadeus"], ["Mozart"], "1756", "1791", style=["Classical"])
cio.createComposerEntry(["Ludwig"], ["van", "Beethoven"], "1770", "1827", style=["Classical"])
cio.createComposerEntry(["Jakob", "Ludwig", "Felix"], ["Mendelssohn", "Bartholdy"], "1770", "1827", known_name="Felix Mendelssohn", style=["Early Romantic"])
