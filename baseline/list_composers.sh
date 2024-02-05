#!/bin/bash

HELPMSG="$(basename ${0})
List all composers in DB"

## PRINT HELP
if [[ "${1}" == "-h" || "${1}" == "--help" ]]; then
  echo "${HELPMSG}"
  exit 0;
fi

if [ -z "${SANCTUS_DB}" ]; then
  echo "Error: DB file is not defined, please set the variable \$SANCTUS_DB"
  exit 1;
fi

RESULT="$(
sqlite3 -readonly -csv "${SANCTUS_DB}" <<EOF
  SELECT firstname, lastname, bornyear, diedyear FROM composers;
EOF
)"

IFS=$'\n'
for LINE in ${RESULT}; do
echo "${LINE}" | cut -d ',' -f 1 | tr -d '"' | tr -d '\n'
echo " " | tr -d '\n'
echo "${LINE}" | cut -d ',' -f 2 | tr -d '"' | tr -d '\n'
echo " (" | tr -d '\n'
echo "${LINE}" | cut -d ',' -f 3 | sed s/'-1'/'?'/g | tr -d '"' | tr -d '\n'
echo " - " | tr -d '\n'
echo "${LINE}" | cut -d ',' -f 4 | sed s/'-1'/'?'/g | tr -d '"' | tr -d '\n'
echo ")"
done