import sys, os
sys.path.append('../')

from db_base.db_composer import Composer_IO
from db_base.db_metadata import Metadata_IO
from db_base.db_score import Score_IO

test_dbpath = os.path.abspath('db_test2/')
c = Composer_IO(test_dbpath)
m = Metadata_IO(test_dbpath)
s = Score_IO(test_dbpath)

#print(c.getComposerInfoExample())
#c.createComposerEntry(["Ludwig"], ["van", "Beethoven"], "1770", "1827")
#c.createComposerEntry(["George", "Frideric"], ["Handel"], "1685", "1759")
#c.createComposerEntry(["Johann", "Sebastian"], ["Bach"], "1685", "1750")
#entry = c._createNewInfoDict(["Johann", "Sebastian"], ["Bach"])
#print(entry)
print(c.deleteComposer("B-l_van_beethoven"))
c.createComposerEntry(["Ludwig"], ["van", "Beethoven"], "1770", "1827")

print(c.queryByNameCode("B-l_van_beethoven"))
print(c.queryByFamilyName("Handel"))
print(c.queryByAbbrName("J.S. Bach"))
print(c.queryByAbbrName("L. van Beethoven"))
print(c.queryByBornYearRange("1700", "1900"))

#m.createItem("piece", title="Werke Nr2", composercode="B-l_van_beethoven", opus="op.2")
#m.updateItem(hashcode='28f6c771b31b42b3dd42be8ad0d3b96e0fa04d58', dkey="Subtitle", new_val="A new sonata")
#m.deleteItem(hashcode='28f6c771b31b42b3dd42be8ad0d3b96e0fa04d58')
#m.createItem("collection", title="Many pieces", composercode="B-l_van_beethoven", opus="op.15")

#m.addWorkInCollection(coll_hashcode='8159147da7357c27263679f3d804400f5bec39f9', new_work_hash='28f6c771b31b42b3dd42be8ad0d3b96e0fa04d58')

print(s.getScoreDirAbs('28f6c771b31b42b3dd42be8ad0d3b96e0fa04d58'))
print(s.getListOfScript('28f6c771b31b42b3dd42be8ad0d3b96e0fa04d58'))

s.createNewEngravingFile('28f6c771b31b42b3dd42be8ad0d3b96e0fa04d58')
