import os, sys
import setup_test

# Testing createDB script

os.system("cd ../scripts && ./create_db.sh -f "+ setup_test.db_abs_path)
