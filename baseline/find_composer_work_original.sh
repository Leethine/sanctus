#!/bin/bash

HELPMSG="$(basename ${0}) [-t TITLE | -o OPUS] [-l LASTNAME | -n KNOWN_NAME | -i COMPOSER_ID] [--simple-display|--pretty-display|--csv-display]
Find composer works"

if [ -z "${SANCTUS_DB}" ]; then
  echo "Error: DB file is not defined, please set the variable \$SANCTUS_DB"
  exit 1;
fi

if [ -z "${SCRIPT_DIR}" ]; then
  SCRIPT_DIR="."
fi

SELECT_COLUMNS="*"
DISPLAY_FORMAT="-line"

# 1. Process arguments
while [[ $# -gt 0 ]]; do
  case ${1} in
    -t|--title)
      TITLE="${2}"
      shift # past argument
      shift # past value
      ;;
    -o|--opus)
      OPUS="${2}"
      shift # past argument
      shift # past value
      ;;
    -n|--composer-knownas-name)
      COMPOSER_KNOWNASNAME="${2}"
      shift # past argument
      shift # past value
      ;;
    -l|--composer-last-name)
      COMPOSER_LASTNAME="${2}"
      shift # past argument
      shift # past value
      ;;
    -i|--composer-id)
      COMPOSER_ID="${2}"
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
    --id-only)
      SELECT_COLUMNS="id"
      DISPLAY_FORMAT="-csv"
      shift # past argument
      ;;
    --check-exist-only)
      CHECK_EXIST="Y"
      DISPLAY_FORMAT="-csv"
      SELECT_COLUMNS="COUNT(id)"
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

# 2. If composer's ID is given, use the id
if [[ ! -z "${COMPOSER_ID}" ]]; then
  COMPOSER_ID=$(sqlite3 -csv "${SANCTUS_DB}" <<EOF
  SELECT id FROM composers WHERE id IS ${COMPOSER_ID};
EOF
  )
  HASCOMPOSER="Y"
  if [[ -z "${COMPOSER_ID}" ]]; then
    echo "The provided composer's ID does not exist"
  fi

# 3. composer's name is given, find composer first
else

  if [[ -z ${COMPOSER_LASTNAME} && ! -z ${COMPOSER_KNOWNASNAME} ]]; then
    COMPOSER_ID=$(${SCRIPT_DIR}/find_composer_exact.sh -n "${COMPOSER_KNOWNASNAME}" --id-only)
    if [[ ! -z "${COMPOSER_ID}" ]]; then
      HASCOMPOSER="Y"
    fi
  elif [[ ! -z ${COMPOSER_LASTNAME} && ! -z ${COMPOSER_KNOWNASNAME} ]]; then
    COMPOSER_ID=$(${SCRIPT_DIR}/find_composer_exact.sh -l "${COMPOSER_LASTNAME}" -n "${COMPOSER_KNOWNASNAME}" --id-only)
    if [[ ! -z "${COMPOSER_ID}" ]]; then
      HASCOMPOSER="Y"
    fi
  elif [[ ! -z ${COMPOSER_LASTNAME} && -z ${COMPOSER_KNOWNASNAME} ]]; then
    COMPOSER_IDS="$(${SCRIPT_DIR}/find_composer_exact.sh -l "${COMPOSER_LASTNAME}" --id-only)"
    if [[ ! -z "${COMPOSER_IDS}" ]]; then
      HASCOMPOSER="M"
    fi
  else
    HASCOMPOSER="N"
  fi

fi

# 4. Compose Title and Opus
SEARCH_COND=""
if [[ ! -z "${TITLE}" ]]; then
  SEARCH_COND="${SEARCH_COND}"" title LIKE '%${TITLE}%' COLLATE NOCASE "
fi
if [[ ! -z "${OPUS}" && ! -z "${TITLE}" ]]; then
  SEARCH_COND="${SEARCH_COND}"" AND opus LIKE '%${OPUS}%' COLLATE NOCASE "
fi
if [[ ! -z "${OPUS}" && -z "${TITLE}" ]]; then
  SEARCH_COND="${SEARCH_COND}"" opus LIKE '%${OPUS}%' COLLATE NOCASE "
fi

# 5. Switch usecases
if [[ ! -z "${SEARCH_COND}" ]]; then
  # no AND if no search condition given
  SEARCH_COND="${SEARCH_COND} AND "
fi

if [[ "${HASCOMPOSER}" == "Y" ]]; then
# Only one composer provided
sqlite3 "${DISPLAY_FORMAT}" "${SANCTUS_DB}" <<EOF
SELECT ${SELECT_COLUMNS} FROM pieces
WHERE ${SEARCH_COND}
composer_id IS '${COMPOSER_ID}';
EOF

elif [[ "${HASCOMPOSER}" == "M" ]]; then
# Multiple composer provided
  ID_COND=""
  for ID in ${COMPOSER_IDS}; do
    ID_COND=" ${ID_COND} composer_id IS ${ID} OR";
  done
  ID_COND="${ID_COND::-2}"

sqlite3 "${DISPLAY_FORMAT}" "${SANCTUS_DB}" <<EOF
SELECT ${SELECT_COLUMNS} FROM pieces
WHERE ${SEARCH_COND}
( ${ID_COND} )
EOF

elif [[ "${HASCOMPOSER}" == "N" ]]; then
# No composer provided
sqlite3 "${DISPLAY_FORMAT}" "${SANCTUS_DB}" <<EOF
SELECT ${SELECT_COLUMNS} FROM pieces
WHERE ${SEARCH_COND}
;
EOF

else
# Composer not found
  echo "Composer '${COMPOSER_LASTNAME} - ${COMPOSER_KNOWNASNAME}' not found"
fi
