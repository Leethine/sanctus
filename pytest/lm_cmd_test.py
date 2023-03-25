import sys
import setup_test
sys.path.append('../..')
sys.path.append('..')

from sanctus.local_mode.command import CommandLine
command_box = CommandLine(setup_test.db_abs_path)
command_box.run()