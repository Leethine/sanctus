#!/bin/bash

DBPATH="${1}"
SQL_SCRIPT="${PWD}/schema.sql"

# Check arguments
if [[ ${1} == "-h" || ${1} == "--help" ]]; then
  printf "Usage:\n${0} PATH_TO_DB \n"
  exit 0;
fi
if [ -z "${DBPATH}" ]; then
  #printf "Invalid arguments! Use '-h' or '--help' to see usage.\n"
  printf "You did not provide a database path...\nUsing default path: ${HOME}/.local/share/sanctus_db\n\n"
  DBPATH="${HOME}/.local/share/sanctus_db"
fi

mkdir -p ${DBPATH}

if [[ -f "${DBPATH}/sanctus.db" ]]; then
  printf "DB already exists:\n ${DBPATH}/sanctus.db\n"
  read -p "Override? [y/N]: " CONFIRM
  if [[ ${CONFIRM} != "y" ]]; then
    echo "Abandoned."
    exit 1;
  fi
fi
echo ""

# Run SQL script
sqlite3 "${DBPATH}/sanctus.db" <<EOF
$(cat ${SQL_SCRIPT})
EOF

echo "${SANCTUS_DB}" >> sanctusenv
export SANCTUS_DB="${DBPATH}/sanctus.db"
echo "DB created at: ${DBPATH}/sanctus.db"
