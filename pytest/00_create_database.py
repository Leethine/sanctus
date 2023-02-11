import os, sys

sys.path.append('..')

from sanctus.db_base.db_composer import Composer_IO
from sanctus.db_base.db_metadata import Metadata_IO
from sanctus.db_base.db_score import Score_IO

curdir = os.path.abspath(os.getcwd())
db_abs_path = curdir + "/" + "__dbtest"

os.system("cd ../scripts && ./create_db.sh -f "+ db_abs_path)