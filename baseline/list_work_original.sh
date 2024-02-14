#!/bin/bash

HELPMSG="$(basename ${0}) [-a ABBRNAME | -l LASTNAME] [--simple-display|--pretty-display|--csv-display]
List all works in DB"

## PRINT HELP
if [[ "${1}" == "-h" || "${1}" == "--help" ]]; then
  echo "${HELPMSG}"
  exit 0;
fi

if [ -z "${SANCTUS_DB}" ]; then
  echo "Error: DB file is not defined, please set the variable \$SANCTUS_DB"
  exit 1;
fi

if [ -z "${SCRIPT_DIR}" ]; then
  SCRIPT_DIR="."
fi

DISPLAY_FORMAT="-list"

# 1. Parse arguments
while [[ $# -gt 0 ]]; do
  case ${1} in
    -l|--last-name)
      LASTNAME="${2}"
      shift # past argument
      shift # past value
      ;;
    -a|--abbr-name)
      ABBRNAME="${2}"
      shift # past argument
      shift # past value
      ;;
    --simple-display)
      SELECT_COLUMNS="*"
      DISPLAY_FORMAT="-list"
      shift # past argument
      ;;
    --pretty-display)
      SELECT_COLUMNS="*"
      DISPLAY_FORMAT="-table"
      shift # past argument
      ;;
    --csv-display)
      SELECT_COLUMNS="*"
      DISPLAY_FORMAT="-csv"
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

# 2. List work by composer's by last name
if [[ ! -z "${LASTNAME}" ]]; then
  ID_COND=""
  for ID in $(${SCRIPT_DIR}/find_composer_exact.sh -l "${LASTNAME}" --id-only); do
    ID_COND="${ID_COND} composer_id IS ${ID} OR"
  done

  if [[ -z "${ID_COND}" ]]; then
    echo "No match found."
    exit 0;
  fi

  ID_COND="${ID_COND::-2}"

sqlite3 -readonly "${DISPLAY_FORMAT}" "${SANCTUS_DB}" <<EOF
  SELECT * FROM pieces
  WHERE ${ID_COND} ;
EOF

# 3. List works by composer's abbreviated name
elif [[ ! -z "${ABBRNAME}" ]]; then
  COMPOSER_ID=$(${SCRIPT_DIR}/find_composer_abbr.sh "${ABBRNAME}" --id-only)

  if [[ -z "${COMPOSER_ID}" ]]; then
    echo "No match found."
    exit 0;
  fi

sqlite3 -readonly "${DISPLAY_FORMAT}" "${SANCTUS_DB}" <<EOF
  SELECT * FROM pieces
  WHERE composer_id IS ${COMPOSER_ID};
EOF

# 3. List all works
else
sqlite3 -readonly "${DISPLAY_FORMAT}" "${SANCTUS_DB}" <<EOF
  SELECT * FROM pieces;
EOF

fi