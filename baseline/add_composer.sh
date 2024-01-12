#!/bin/bash

if [ -z "${SANCTUS_DB}" ]; then
  echo "Error: DB file is not defined, please set the variable \$SANCTUS_DB"
  exit 1;
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
EXIST=$(./find_composer.sh -l "${LASTNAME}" -f "${FIRSTNAME}" --id-only)
if [[ ! -z "${EXIST}" && -z "${ALLOW_DUPLICATE}" ]]; then
  echo "Composer already existed, if you are sure, please use --allow-duplicate"
  exit 0;
fi

# 6. Run SQL script
sqlite3 "${SANCTUS_DB}" <<EOF
INSERT INTO composers (firstname, lastname, knownas_name, bornyear, diedyear)
VALUES('${FIRSTNAME}','${LASTNAME}','${KNOWNASNAME}','${BORNYEAR}','${DIEDYEAR}');
EOF

# 7. Log the inserted data
if [ -z ${NO_OUTPUT} ]; then
echo "Added composer in ${SANCTUS_DB}"
echo "Last name: ${LASTNAME}"
echo "First name: ${FIRSTNAME}"
echo "Known as: ${KNOWNASNAME}"
echo "Born year: ${BORNYEAR_STR}"
echo "Died year: ${DIEDYEAR_STR}"
fi