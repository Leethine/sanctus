#!/bin/bash

HELPMSG="$(basename ${0}) -f FIRSTNAME -l LASTNAME -n KNOWN_AS -b BORN -d DIED [--allow-duplicate] [--quiet]
Add new composer in DB."

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

# 1. Process arguments
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
    -b|--born-year)
      BORNYEAR="${2}"
      shift # past argument
      shift # past value
      ;;
    -d|--died-year)
      DIEDYEAR="${2}"
      shift # past argument
      shift # past value
      ;;
    --allow-duplicate)
      ALLOW_DUPLICATE="Y"
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

# 2. Check missing args
BORNYEAR_STR="${BORNYEAR}"
DIEDYEAR_STR="${DIEDYEAR}"
if [ -z "${LASTNAME}" ]; then
  echo "Missing mandatory argument: '--last-name'"
  exit 1;
fi
if [ -z "${FIRSTNAME}" ]; then
  echo "Missing mandatory argument: '--first-name'"
  exit 1;
fi
if [ -z "${KNOWNASNAME}" ]; then
  echo "Missing mandatory argument: '--known-as'"
  exit 1;
fi

# 3. Convert born year and died year to correct formats
if [[ -z "${BORNYEAR}" ]]; then
  BORNYEAR=-1
  BORNYEAR_STR="?"
fi
if [[ -z "${DIEDYEAR}" ]]; then
  DIEDYEAR=-1
  DIEDYEAR_STR="?"
fi
if [[ "${BORNYEAR}" =~ [[:alpha:]] ]]; then
  echo "Invalid argument format: '--born-year'"
  exit 1;
fi
if [[ "${DIEDYEAR}" =~ [[:alpha:]] ]]; then
  echo "Invalid argument format: '--died-year'"
  exit 1;
fi

# 4. Clean up extra spaces in composer name
FIRSTNAME="$(echo "$FIRSTNAME" | tr -s ' ')"
LASTNAME="$(echo "$LASTNAME" | tr -s ' ')"
KNOWNASNAME="$(echo "$KNOWNASNAME" | tr -s ' ')"

# 5. Check if composer already existed
EXISTED=$(${SCRIPT_DIR}/find_composer_exact.sh -l "${LASTNAME}" -n "${KNOWNASNAME}" --check-exist-only)
if [[ ! -z "${EXISTED}" && ${EXISTED} =~ '^[0-9]+$' && -z "${ALLOW_DUPLICATE}" ]]; then
  echo "Composer already existed, if you are sure to create, please use --allow-duplicate"
  exit 0;
fi

# 6. Run SQL script to insert into composer table
sqlite3 "${SANCTUS_DB}" <<EOF
INSERT INTO composers (firstname, lastname, knownas_name, bornyear, diedyear)
VALUES('${FIRSTNAME}','${LASTNAME}','${KNOWNASNAME}','${BORNYEAR}','${DIEDYEAR}');
EOF

# 7. Calculate composer active year and insert into composers_mid_year table
if [[ ! ${BORNYEAR} -eq -1 && ! ${DIEDYEAR} -eq -1 ]]; then
  YEAR_MID=$(((${BORNYEAR}+${DIEDYEAR})/2))
  COMPOSER_ID=$(${SCRIPT_DIR}/find_composer_exact.sh -l "${LASTNAME}" -n "${KNOWNASNAME}" --id-only)

sqlite3 "${SANCTUS_DB}" <<EOF
  INSERT INTO composers_mid_year (id, year_mid)
  VALUES(${COMPOSER_ID},${YEAR_MID});
EOF
fi

# 8. Log the inserted data
if [ -z ${NO_OUTPUT} ]; then
  echo "Added composer in ${SANCTUS_DB}"
  echo "Last name: ${LASTNAME}"
  echo "First name: ${FIRSTNAME}"
  echo "Known as: ${KNOWNASNAME}"
  echo "Born year: ${BORNYEAR_STR}"
  echo "Died year: ${DIEDYEAR_STR}"
fi
