#!/bin/bash

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
    -t|--title)
      TITLE="${2}"
      shift # past argument
      shift # past value
      ;;
    -s|--subtitle)
      SUBTITLE="${2}"
      shift # past argument
      shift # past value
      ;;
    -x|--subsubtitle)
      SUBSUBTITLE="${2}"
      shift # past argument
      shift # past value
      ;;
    -c|--composer-id)
      COMPOSER_ID="${2}"
      shift # past argument
      shift # past value
      ;;
    -n|--composer-knownas-name)
      COMPOSER_KNOWNASNAME="${2}"
      shift # past argument
      shift # past value
      ;;
    -a|--composer-abbrname)
      COMPOSER_ABBRNAME="${2}"
      shift # past argument
      shift # past value
      ;;
    -o|--opus)
      OPUS="${2}"
      shift # past argument
      shift # past value
      ;;
    -i|--instrument)
      INSTRUMENT="${2}"
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


# 2. Check input arguments, only one argument should be used
#TBD

# 3. Find composer first
if [[ ! -z "${COMPOSER_KNOWNASNAME}" && -z "${COMPOSER_ABBRNAME}" ]]; then
  COMPOSER_ID=$(${SCRIPT_DIR}/find_composer_exact.sh -n "${KNOWNASNAME}" --id-only)
elif [[ ! -z "${COMPOSER_ABBRNAME}" && -z "${COMPOSER_KNOWNASNAME}" ]]; then
  CHECK_DUP=$(${SCRIPT_DIR}/find_composer_abbr.sh "${COMPOSER_ABBRNAME}" --check-duplication)
  if [[ ${CHECK_DUP} -gt 1 ]]; then
    echo "Warning: More than one composer is named: ${COMPOSER_ABBRNAME}"
    COMPOSER_ID=-1
  else
    COMPOSER_ID=$(${SCRIPT_DIR}/find_composer_abbr.sh "${COMPOSER_ABBRNAME}" --id-only)
  fi
else
  echo "Warning: homeless work ${TITLE} ${OPUS} (No assiciated composer)"
  COMPOSER_ID=-1
fi

# 4. Check duplicity
#if [[ "${ALLOW_DUPLICATE}" != "Y" ]]; then
# TBD
#fi

# 5. Insert to DB
sqlite3 "${SANCTUS_DB}" <<EOF
  INSERT INTO pieces
  (composer_id, collection_id, title, subtitle, subsubtitle, opus, instrument)
  VALUES(${COMPOSER_ID},-2,'${TITLE}',
  '${SUBTITLE}','${SUBSUBTITLE}','${OPUS}','${INSTRUMENT}');
EOF

echo "Inserted work."