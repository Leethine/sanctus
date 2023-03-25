import os, sys
sys.path.append('../..')
sys.path.append('..')
import setup_test

from sanctus.db_base.db_composer import Composer_IO

# Connect to DB
cio = Composer_IO(setup_test.db_abs_path)

# Clean database
cio.deleteComposerForce("F-g_a_frescobaldi")
cio.deleteComposerForce("H-g_f_handel")
cio.deleteComposerForce("B-j_s_bach")
cio.deleteComposerForce("M-w_a_mozart")
cio.deleteComposerForce("B-l_van_beethoven")
cio.deleteComposerForce("M-j_l_f_mendelssohn_bartholdy")