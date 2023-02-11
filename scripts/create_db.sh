#!/bin/bash
# Create DB in DATA_DIR
# Usage:
#   create_db.sh "DATA_DIR"

usage()
{
  echo 'Usage: $(basename $0) [-h| ] "DATA_DIR"'
}

confirm_override_db_dir()
{
  DATA_DIR="${1}"
  # Creation check
  if [ ! -d "${DATA_DIR}" ]; then
    echo "Creating DB in ${DATA_DIR}"
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
}

force_override_db_dir()
{
  DATA_DIR="${1}"
  # Creation if directory not already exists
  if [[ ! -d "${DATA_DIR}" && -f "${DATA_DIR}" ]]; then
    rm "${DATA_DIR}"
  elif [ ! -d "${DATA_DIR}" ]; then
    echo "Creating DB in ${DATA_DIR}"
    mkdir "${DATA_DIR}"
  # Override directory if already exists
  else
    rm -fr "${DATA_DIR}"
    mkdir "${DATA_DIR}"
  fi
}

descriptor_creation()
{
  cd "${3}"
  "${1}"/create_db_desc.py "${PWD}" "${2}"
  cd ..
}

db_file_creation()
{
  DATA_DIR="${1}"
  RUN_PWD="${2}"

  cd "${DATA_DIR}"

  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  echo "Info: creating subdirectories in ${PWD}"

  # Create 3 main directories
  mkdir composer metadata score
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" composer
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" metadata
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" score

  # Create composer db
  cd composer
  "${RUN_PWD}"/create_db_desc.py "${PWD}" "${DATA_DIR}"
  echo "Info: creating subdirectories in ${PWD}"
  mkdir info icon biography
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" info
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" icon
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" biography

  # go back to root_dir
  cd ..
  
  # Create metadata db
  cd metadata
  echo "Info: creating subdirectories in ${PWD}"
  mkdir arrangement collection piece template
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" arrangement
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" collection
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" piece
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" template

  # go back to root dir
  cd ..

  cd score
  echo "Info: in ${PWD}"
  echo "Creating sha-1 hash subdirectories..."
  mkdir 0 1 2 3 4 5 6 7 8 9 a b c d e f
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" 0
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" 1
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" 2
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" 3
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" 4
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" 5
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" 6
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" 7
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" 8
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" 9
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" a
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" b
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" c
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" d
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" e
  descriptor_creation "${RUN_PWD}" "${DATA_DIR}" f

  echo "done"
  cd ../..

  echo "DB created in ${DATA_DIR}"
  exit 0
}



#### RUNNING ####

# Check arguments
# Check if the number of input arguments is correct
if [ $# -eq 0 ]; then
  echo "Error: no arguments provided."
  usage
  exit 1
fi
# Check if help message is requested
if [[ "${1}" == "-h" ]] || [[ "${1}" == "--help" ]]; then
  echo "Help: This script creates DB in \$DATA_DIR"
  usage
  exit 0
fi

# Check if force DB creation
if [ $# -eq 2 ] && [[ "${1}" == "-f" || "${1}" == "--force" ]]; then
  DATA_DIR="$(realpath "${2}")"
  force_override_db_dir "${DATA_DIR}"
  db_file_creation "${DATA_DIR}" "${PWD}"
elif [ $# -eq 1 ] && [[ ! -d "${1}" && -f "${1}" ]]; then
  # Check if directory name is occupied by an existing file
  echo "Input Error: '${1}' - file exists"
  exit 1
else # No file name conflict
  DATA_DIR="$(realpath "${1}")"
  confirm_override_db_dir "${DATA_DIR}"
  db_file_creation "${DATA_DIR}" "${PWD}"
fi
