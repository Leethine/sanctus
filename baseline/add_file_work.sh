#!/bin/bash

if [ -z "${SANCTUS_DB}" ]; then
  echo "Error: DB file is not defined, please set the variable \$SANCTUS_DB"
  exit 1;
fi

if [ -z "${SCRIPT_DIR}" ]; then
  SCRIPT_DIR="."
fi

# 1. Process arguments
while [[ $# -gt 0 ]]; do
  case ${1} in
    -i|--piece-id)
      PIECE_ID="${2}"
      shift # past argument
      shift # past value
      ;;
    -n|--file-name)
      FILENAME="${2}"
      shift # past argument
      shift # past value
      ;;
    -e|--extension)
      EXTENSION="${2}"
      shift # past argument
      shift # past value
      ;;
    -c|--comment)
      COMMENT="${2}"
      shift # past argument
      shift # past value
      ;;
    --arranged)
      ARRANGED="Y"
      shift # past argument
      ;;
    --quiet)
      NO_OUTPUT="Y"
      shift # past argument
      ;;
    -*|--*)
      echo "Unknown option ${1}"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("${1}") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

# 2. Check important argument
if [[ -z "${PIECE_ID}" ]]; then
  echo "Cannot create homeless file."
  exit 0;
fi

# 3. Check if piece exists
if [[ "${ARRANGED}" == "Y" ]]; then
  ISARRANGED=1
  PIECE_TITLE="$(sqlite3 -readonly -csv "${SANCTUS_DB}" <<EOF
    SELECT title FROM arranged_pieces WHERE id = ${PIECE_ID};
EOF
)"

else
  ISARRANGED=0
  PIECE_TITLE="$(sqlite3 -readonly -csv "${SANCTUS_DB}" <<EOF
    SELECT title FROM pieces WHERE id = ${PIECE_ID};
EOF
)"
fi

if [[ -z "${PIECE_TITLE}" ]]; then
  echo "Piece ID: ${PIECE_ID} does not exist."
  exit 0;
fi

# 4. Get the file_number to insert
LAST_FILE_NUMBER=$(sqlite3 -readonly "${SANCTUS_DB}" <<EOF
  SELECT MAX(file_number) FROM files WHERE piece_id = ${PIECE_ID};
EOF
)
if [[ -z ${LAST_FILE_NUMBER} ]]; then
  NEW_FILE_NUMBER=0
else
  NEW_FILE_NUMBER=$((${LAST_FILE_NUMBER}+1))
fi

# 5. Get the file hash
SHA1HASH="$(echo "SANCTUS-${PIECE_ID}-SUTCNAS" | sha1sum | cut -d ' ' -f 1 )"

# 6. Insert into DB
if [[ -z "${EXTENSION}" ]]; then
  # default extension is ly (lilypond)
  EXTENSION="ly"
fi

sqlite3 ${SANCTUS_DB} <<EOF
  INSERT INTO files
  (piece_id, is_arranged, file_number, file_name, extension, folder_hash, comment)
  VALUES
  (${PIECE_ID},${ISARRANGED},${NEW_FILE_NUMBER},'${FILENAME}_${NEW_FILE_NUMBER}.${EXTENSION}',
  '${EXTENSION}','${SHA1HASH}','${COMMENT}');
EOF

