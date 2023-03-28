import sys, os
sys.path.append('../')

from db_base.cli_adapter import DataBaseCliAdapter
test_dbpath = os.path.abspath('db_test/')
print(test_dbpath)
cli = DataBaseCliAdapter(test_dbpath)
print(cli.findComposer("abbrname", "L. Beethoven"))
print(cli.findComposer("year", "1000-2000"))