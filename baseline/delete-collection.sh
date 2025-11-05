#!/bin/bash

# Check env
if [ -z "${SANCTUS_DATAPATH}" ]; then
  echo "env variable SANCTUS_DATAPATH not defined"
  exit 1
fi
if [ -z "${SANCTUS_DB}" ]; then
  DBFILE="${SANCTUS_DATAPATH}/tables.db"
else
  DBFILE="${SANCTUS_DB}"
fi
if [ -z "${SANCTUS_FS}" ]; then
  FSPATH="${SANCTUS_DATAPATH}/files"
else
  FSPATH="${SANCTUS_FS}"
fi


COLLECTION_CODE="${1}"
FORCE="${2}"


EXISTING="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT code FROM collections WHERE
  code = '${COLLECTION_CODE}';
EOF
)"

if [ ! -z "${EXISTING}" ]; then

  if [ -z "${FORCE}" ]; then 
    read -p "Delete collection from DB? [y/N]:" CONFIRM
  else
    CONFIRM="y"
  fi

  # Delete from DB
  if [[ ${CONFIRM} != "y" ]]; then
    echo "Abandoned."
    exit 0

  else

sqlite3 -csv "${DBFILE}" <<EOF
  DELETE FROM collections WHERE
  code = '${COLLECTION_CODE}';
EOF
  echo "Deleted collection ${COLLECTION_CODE} from DB."
  fi

else
  echo "No matching piece found: ${COLLECTION_CODE}"
fi
