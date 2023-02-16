import os, sys
sys.path.append('..')
import setup_test

from sanctus.db_base.db_composer import Composer_IO

"""
Testing db_base/db_composer.py base class
Query
"""

# Connect to DB
cio = Composer_IO(setup_test.db_abs_path)

# Check insertion by querying composer info
print("")
print("Testing query...")
print("")

print("queryByAbbrName - \"J.S. Bach\":")
print(cio.queryByAbbrName("J.S. Bach")[0]["FullName"])
print("")

print("queryByFamilyName - \"Mendelssohn\":")
print(cio.queryByFamilyName("Mendelssohn")[0]["FullName"])
print("")

print("queryByBornYearRange - \"1582 - 1584\":")
print(cio.queryByBornYearRange(1582, 1584)[0]["FullName"])
print("")

print("queryByDiedYearRange - \"1790 - 1792\":")
print(cio.queryByDiedYearRange(1790, 1792)[0]["FullName"])
print("")