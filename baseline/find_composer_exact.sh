#!/bin/bash

if [ -z "${SANCTUS_DB}" ]; then
  echo "Error: DB file is not defined, please set the variable \$SANCTUS_DB"
  exit 1;
fi

SELECT_COLUMNS="*"
DISPLAY_FORMAT="-line"

# 1. Parse arguments
while [[ $# -gt 0 ]]; do
  case ${1} in
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

if [[ ! -z "${LASTNAME}" && -z "${KNOWNASNAME}" ]]; then
sqlite3 -readonly ${DISPLAY_FORMAT} "${SANCTUS_DB}" <<EOF
  SELECT ${SELECT_COLUMNS} FROM composers
  WHERE lastname IS '${LASTNAME}' COLLATE NOCASE;
EOF
elif [[ -z "${LASTNAME}" && ! -z "${KNOWNASNAME}" ]]; then
sqlite3 -readonly ${DISPLAY_FORMAT} "${SANCTUS_DB}" <<EOF
  SELECT ${SELECT_COLUMNS} FROM composers
  WHERE knownas_name IS '${KNOWNASNAME}' COLLATE NOCASE;
EOF
elif [[ ! -z "${LASTNAME}" && ! -z "${KNOWNASNAME}" ]]; then
sqlite3 -readonly ${DISPLAY_FORMAT} "${SANCTUS_DB}" <<EOF
  SELECT ${SELECT_COLUMNS} FROM composers
  WHERE lastname IS '${LASTNAME}' AND knownas_name IS '${KNOWNASNAME}' COLLATE NOCASE;
EOF
else
  echo "Error: bad arguments, use --help for more information."
  exit 1;
fi
