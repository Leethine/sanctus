#!/bin/bash

if [[ -z "${SANCTUS_DB}" ]]; then
  echo "Error: DB file is not defined, please set the variable \$SANCTUS_DB"
  exit 1;
fi

# 1. Parse arguments
if [[ "${1}" == "--help" || "${1}" == "-h" ]]; then
  echo "Usage:"
fi

YEARBEGIN="${1}"
YEAREND="${2}"

if [[ "${3}" == "--pretty-display" ]]; then
  SELECT_COLUMNS="*"
  DISPLAY_FORMAT="-table"
elif [[ "${3}" == "--id-only" ]]; then
  SELECT_COLUMNS="id"
  DISPLAY_FORMAT="-csv"
elif [[ "${3}" == "--csv-display" ]]; then
  SELECT_COLUMNS="*"
  DISPLAY_FORMAT="-csv"
else
  SELECT_COLUMNS="*"
  DISPLAY_FORMAT="-line"
fi

# 2. Select based on years
IDLIST="$(
sqlite3 -readonly -csv "${SANCTUS_DB}" <<EOF
  SELECT id FROM composers_mid_year
  WHERE year_mid >= ${YEARBEGIN} AND year_mid <= ${YEAREND};
EOF
)"

# 3. Construct search conditions (id to search)
ID_TO_SEARCH="id == 0 "
IFS=$'\n'
for ID in ${IDLIST}; do
  ID_TO_SEARCH="${ID_TO_SEARCH}"" OR id == ${ID}"
done

# 4. Search in SQL
sqlite3 -readonly "${DISPLAY_FORMAT}" "${SANCTUS_DB}" <<EOF
  SELECT ${SELECT_COLUMNS} FROM composers
  WHERE ${ID_TO_SEARCH}
  ;
EOF
