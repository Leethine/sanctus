#!/bin/bash
# Create DB in DATA_DIR
# Usage:
#   create_db.sh "DATA_DIR"

usage()
{
  echo 'Usage: $(basename $0) -h | "DATA_DIR"'
}

if [ $# -eq 0 ]; then
  echo "Error: no arguments provided."
  usage
  exit 1
fi

if [[ "${1}" == "-h" ]] || [[ "${1}" == "--help" ]]; then
  echo "Help: This script creates DB in \$DATA_DIR"
  usage
  exit 0
fi

if [[ ! -d "${1}" && -f "${1}" ]]; then
  echo "Input Error: '${1}' - file exists"
  exit 1

else # Input argument OK
  RUN_PWD="${PWD}"
  DATA_DIR="$(realpath "${1}")"

  # Creation check
  if [ ! -d "${DATA_DIR}" ]; then
    echo "Creating DB in ${DATA_DIR} ..."
    read -p "Confirm? [Y/n]"$'\n' -r reply_input
    echo ""
    if [[ "${reply_input}" =~ ^[Yy] ]]; then
      mkdir "${DATA_DIR}"
    else
      echo "Abandoned."
      exit 0
    fi
  # Override check
  else
    read -p "Directory already exists, override? [Y/n]"$'\n' -r reply_input
    echo ""
    if [[ "${reply_input}" =~ ^[Yy] ]]; then
      rm -fr "${DATA_DIR}"
      mkdir "${DATA_DIR}"
    else
      echo "Abandoned."
      exit 0
    fi
  fi

  cd "${DATA_DIR}"
  echo "Info: creating subdirectories in ${PWD}"

  # Create 3 main directories
  mkdir composer metadata score
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"

  # Create composer db
  cd composer
  echo "Info: creating subdirectories in ${PWD}"
  mkdir info oeuvre icon biography
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"

  cd info
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  cd ..

  cd oeuvre
  mkdir ac b def ghij kl mnopq rtuvwxyz s
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  for dir in $(ls -d */); do
    cd $dir
    "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
    cd ..
  done
  cd ..

  cd icon
  mkdir ac b def ghij kl mnopq rtuvwxyz s
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  for dir in $(ls -d */); do
    cd $dir
    "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
    cd ..
  done
  cd ..

  cd biography
  mkdir ac b def ghij kl mnopq rtuvwxyz s
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  for dir in $(ls -d */); do
    cd $dir
    "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
    cd ..
  done
  cd ..

  # go back to root_dir
  cd ..
  
  # Create metadata db
  cd metadata
  echo "Info: creating subdirectories in ${PWD}"
  mkdir arrangement collection piece template
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"

  cd template
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  cd ..

  cd arrangement
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  cd ..

  cd collection
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  cd ..

  cd piece
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  cd ..

  # go back to root dir
  cd ..

  cd score
  echo "Info: creating subdirectories in ${PWD}"
  mkdir file template
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"

  cd template
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  cd ..

  cd file

  echo "Info: in ${PWD}"
  echo "Creating sha-1 hash subdirectories..."
  mkdir 0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"

  for dir in $(ls -d */); do
    cd $dir
    "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
    cd ..
  done

  echo "done"
  cd ../..

  echo "DB created in ${DATA_DIR}"
  exit 0
fi