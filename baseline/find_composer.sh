#!/bin/bash

if [ -z "${SANCTUS_DB}" ]; then
  echo "Error: DB file is not defined, please set the variable \$SANCTUS_DB"
  exit 1;
fi

SELECT_COLUMNS="*"
DISPLAY_FORMAT="-line"

# 1. Pass arguments
while [[ $# -gt 0 ]]; do
  case ${1} in
    -f|--first-name)
      FIRSTNAME="${2}"
      shift # past argument
      shift # past value
      ;;
    -l|--last-name)
      LASTNAME="${2}"
      shift # past argument
      shift # past value
      ;;
    -n|--known-as)
      KNOWNASNAME="${2}"
      shift # past argument
      shift # past value
      ;;
    -a|--abbreviaion)
      ABBRNAME="${2}"
      shift # past argument
      shift # past value
      ;;
    --id-only)
      SELECT_COLUMNS="id"
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

# 2. Clean up input search criteria
FIRSTNAME="$(echo "$FIRSTNAME" | tr -s ' ')"
LASTNAME="$(echo "$LASTNAME" | tr -s ' ')"
KNOWNASNAME="$(echo "$KNOWNASNAME" | tr -s ' ')"
ABBRNAME="$(echo "$ABBRNAME" | tr -s ' ')"

# 3. Check if arguments are passed
if [[ -z "${LASTNAME}" && -z "${FIRSTNAME}" && -z "${KNOWNASNAME}" && -z "${ABBRNAME}" ]]; then
  echo "Error: Search critera should be provided, use --help for more information."
  exit 1;
fi

# 4. Run SQL script depending on search criteria
if [[ ! -z "${LASTNAME}" && -z "${FIRSTNAME}" ]]; then
sqlite3 -readonly ${DISPLAY_FORMAT} "${SANCTUS_DB}" <<EOF
  SELECT ${SELECT_COLUMNS} FROM composers
  WHERE lastname IS '${LASTNAME}' COLLATE NOCASE;
EOF
elif [[ -z "${LASTNAME}" && ! -z "${FIRSTNAME}" ]]; then
sqlite3 -readonly ${DISPLAY_FORMAT} "${SANCTUS_DB}" <<EOF
  SELECT ${SELECT_COLUMNS} FROM composers
  WHERE firstname IS '${FIRSTNAME}' COLLATE NOCASE;
EOF
elif [[ ! -z "${LASTNAME}" && ! -z "${FIRSTNAME}" ]]; then
sqlite3 -readonly ${DISPLAY_FORMAT} "${SANCTUS_DB}" <<EOF
  SELECT ${SELECT_COLUMNS} FROM composers
  WHERE lastname IS '${LASTNAME}' COLLATE NOCASE
  AND firstname IS '${FIRSTNAME}' COLLATE NOCASE;
EOF
elif [[ ! -z "${KNOWNASNAME}" ]]; then
sqlite3 -readonly ${DISPLAY_FORMAT} "${SANCTUS_DB}" <<EOF
  SELECT ${SELECT_COLUMNS} FROM composers
  WHERE knownas_name IS '${KNOWNASNAME}' COLLATE NOCASE;
EOF
elif [[ ! -z "${ABBRNAME}" ]]; then
sqlite3 -readonly ${DISPLAY_FORMAT} "${SANCTUS_DB}" <<EOF
  SELECT ${SELECT_COLUMNS} FROM composers
  WHERE knownas_name IS '${ABBRNAME}' COLLATE NOCASE;
EOF
else
  echo "Error: Wrong arguments, use --help for more information."
  exit 1;
fi