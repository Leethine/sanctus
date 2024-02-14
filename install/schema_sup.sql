------------------------------------------------
-- The tables below are for analysis purposes --
------------------------------------------------
DROP TABLE IF EXISTS tonality_original_piece;
CREATE TABLE tonality_original_piece (
  piece_id INTEGER NOT NULL;
  tonality TEXT;
);