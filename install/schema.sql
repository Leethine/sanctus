-- Table to store composers --
DROP TABLE IF EXISTS composers;
CREATE TABLE composers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  knownas_name TEXT UNIQUE NOT NULL,
  bornyear INTEGER,
  diedyear INTEGER
);

-- Table to store composers "active" year --
DROP TABLE IF EXISTS composers_mid_year;
CREATE TABLE composers_mid_year (
  id INTEGER,
  year_mid INTEGER
);

-- Table to store collections --
DROP TABLE IF EXISTS collections;
CREATE TABLE collections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  subtitle TEXT,
  subsubtitle TEXT,
  description_text TEXT,
  volume INTEGER,
  composer_id INTEGER,
  editor TEXT,
  opus TEXT
);

-- Table to store single pieces --
DROP TABLE IF EXISTS pieces;
CREATE TABLE pieces (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  composer_id INTEGER,
  collection_id INTEGER,
  title TEXT NOT NULL,
  subtitle TEXT,
  subsubtitle TEXT,
  opus TEXT,
  instrument TEXT
);

-- Table to store single (arranged) pieces --
DROP TABLE IF EXISTS arranged_pieces;
CREATE TABLE arranged_pieces (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  original_piece_id INTEGER,
  composer_id INTEGER,
  collection_id INTEGER,
  arranger_id INTEGER,
  arranger_name TEXT,
  title TEXT NOT NULL,
  subtitle TEXT,
  subsubtitle TEXT,
  opus TEXT,
  instrument TEXT
);

-- Table to store actual files --
DROP TABLE IF EXISTS files;
CREATE TABLE files (
  file_number INTEGER PRIMARY KEY AUTOINCREMENT,
  file_hash TEXT NOT NULL,
  file_name TEXT NOT NULL,
  piece_id INTEGER,
  is_arranged BOOLEAN DEFAULT 0,
  format TEXT,
  creation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_modification_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  comment TEXT
);
