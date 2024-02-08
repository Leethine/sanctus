#!/bin/bash

HELPMSG="$(basename ${0}) ABBRNAME [--pretty-display|--id-only|--csv-display] [--check-duplication]
Find composer by abbreviated name."

## PRINT HELP
if [[ "${1}" == "-h" || "${1}" == "--help" ]]; then
  echo "${HELPMSG}"
  exit 0;
fi

if [[ -z "${SANCTUS_DB}" ]]; then
  echo "Error: DB file is not defined, please set the variable \$SANCTUS_DB"
  exit 1;
fi

if [ -z "${SCRIPT_DIR}" ]; then
  SCRIPT_DIR="."
fi

# 1. Parse arguments
if [[ "${1}" == "--help" || "${1}" == "-h" ]]; then
  echo "Usage:"
fi
ABBR_NAME="${1}"

if [[ "${2}" == "--pretty-display" ]]; then
  SELECT_COLUMNS="*"
  DISPLAY_FORMAT="-table"
elif [[ "${2}" == "--id-only" ]]; then
  SELECT_COLUMNS="id"
  DISPLAY_FORMAT="-csv"
elif [[ "${2}" == "--csv-display" ]]; then
  SELECT_COLUMNS="*"
  DISPLAY_FORMAT="-csv"
elif [[ "${2}" == "--check-duplication" ]]; then
  SELECT_COLUMNS="COUNT(*)"
  DISPLAY_FORMAT="-csv"
else
  SELECT_COLUMNS="*"
  DISPLAY_FORMAT="-line"
fi

# 2. Fist find all candidates by last name
ABBRNAME_LC="$(echo ${ABBR_NAME} | tr '[:upper:]' '[:lower:]')"
LASTNAME="$(echo ${ABBRNAME_LC} | rev | cut -d ' ' -f 1 | rev)"
QUERY_RESULT="$(sqlite3 -readonly -csv "${SANCTUS_DB}" <<EOF
  SELECT * FROM composers
  WHERE knownas_name LIKE '%${LASTNAME}%' COLLATE NOCASE;
EOF
)"

# 3. Match known-as name with abbr name, stop the for loop when match is found
IFS=$'\n'
MATCHFOUND=0
for LINE in ${QUERY_RESULT}; do
  CANDIDATE_ID="$(echo "${LINE}" | cut -d ',' -f 1)"
  # Process match strings
  CANDIDATE_KNOWNASNAME="$(echo "${LINE}" | cut -d ',' -f 4 | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr -d '"')"
  CANDIDATE_FIRSTNAME="$(echo "${CANDIDATE_KNOWNASNAME}" | sed s/"_${LASTNAME}"//g)"
  CANDIDATE_LASTNAME="${LASTNAME}"
  SEARCH_ABBRNAME="$(echo ${ABBR_NAME} | tr ' ' '_')"
  ISMATCH=$(${SCRIPT_DIR}/../toolbox/match_name_abbr.pl ${CANDIDATE_FIRSTNAME} ${CANDIDATE_LASTNAME} ${SEARCH_ABBRNAME})
  if [[ ${ISMATCH} -eq 1 ]]; then
    MATCHFOUND=1
    break;
  fi
done

# 4. Display the result
if [[ ${ISMATCH} -eq 1 && ${MATCHFOUND} -eq 1 ]]; then
sqlite3 -readonly "${DISPLAY_FORMAT}" "${SANCTUS_DB}" <<EOF
  SELECT ${SELECT_COLUMNS} FROM composers
  WHERE id IS '${CANDIDATE_ID}';
EOF
else
  echo "No match found."
fi
