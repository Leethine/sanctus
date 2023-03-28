# constants.py
# Defines constants

DEFAULT_LOCAL_DB_DIR = "/home/Music/my_score_sanctus"
DEFAULT_SERVER_DB_DIR = "/tmp/sanctus_db"

DEFAULT_DB_DIR_PATH=DEFAULT_LOCAL_DB_DIR

DEFAULT_LANG = "en"
DEFAULT_NS = "EN"
DEFAULT_ENGRAVOR = "lilypond"
DEFAULT_GUI = "frescobaldi"
DEFAULT_EXTENTION = ".ly"

DEFAULT_HOST = "sanctus.host"
DEFAULT_PORT = 9999

ROOTPATH = "$ROOT"

DB_NON_VALID_ERR = -2

CONFIG_NON_VALID_ERR = -3

# DB parition according to family name initial
COMPOSER_NAME_PARTITION_MAP = {
  "a": "ac",
  "b": "b",
  "c": "ac",
  "d": "def",
  "e": "def",
  "f": "def",
  "g": "ghij",
  "h": "ghij",
  "i": "ghij",
  "j": "ghij",
  "k": "kl",
  "l": "kl",
  "m": "mnopq",
  "n": "mnopq",
  "o": "mnopq",
  "p": "mnopq",
  "q": "mnopq",
  "r": "rtuvwxyz",
  "s": "s",
  "t": "rtuvwxyz",
  "u": "rtuvwxyz",
  "v": "rtuvwxyz",
  "w": "rtuvwxyz",
  "x": "rtuvwxyz",
  "y": "rtuvwxyz",
  "z": "rtuvwxyz",
  "A": "ac",
  "B": "b",
  "C": "ac",
  "D": "def",
  "E": "def",
  "F": "def",
  "G": "ghij",
  "H": "ghij",
  "I": "ghij",
  "J": "ghij",
  "K": "kl",
  "L": "kl",
  "M": "mnopq",
  "N": "mnopq",
  "O": "mnopq",
  "P": "mnopq",
  "Q": "mnopq",
  "R": "rtuvwxyz",
  "S": "s",
  "T": "rtuvwxyz",
  "U": "rtuvwxyz",
  "V": "rtuvwxyz",
  "W": "rtuvwxyz",
  "X": "rtuvwxyz",
  "Y": "rtuvwxyz",
  "Z": "rtuvwxyz"
}