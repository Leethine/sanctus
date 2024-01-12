#!/bin/bash
# EXPERIMENTAL - NOT in use

DBPATH="${1}"
USERNAME="${2}"

# Check arguments
if [[ ${1} == "-h" || ${1} == "--help" ]]; then
  printf "Usage:\n${0} FILEPATH [USERNAME]\n"
  exit 0;
fi
if [ -z "${DBPATH}" ]; then
  printf "Invalid arguments! Use '-h' or '--help' to see usage.\n"
  exit 0;
fi

# Create filesystem directory

#DBPATH="$(realpath ${DBPATH})" 
SUBDIR="sanctus_fs/default"

if [ ! -z "${USERNAME}" ]; then
  SUBDIR="sanctus_fs/${USERNAME}"
fi

# Create subdirectories for the files' sha-1 hash
mkdir -p "${DBPATH}/${SUBDIR}"
cd "${DBPATH}/${SUBDIR}"

for i in {0..9}{a..f}; do
  mkdir ${i}
done

for i in {a..f}{0..9}; do
  mkdir ${i}
done

cd ../..
chmod --recursive a+rwx "${SUBDIR}"

exit 0;