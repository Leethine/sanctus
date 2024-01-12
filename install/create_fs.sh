#!/bin/bash

FSPATH="${1}"

# Check arguments
if [[ ${1} == "-h" || ${1} == "--help" ]]; then
  printf "Usage:\n${0} PATH_TO_FILESYSTEM \n"
  exit 0;
fi
if [ -z "${FSPATH}" ]; then
  #printf "Invalid arguments! Use '-h' or '--help' to see usage.\n"
  printf "You did not provide a filesystem path...\n Using default path: ${HOME}/.local/share\n\n"
  FSPATH="${HOME}/.local/share"
fi

# Check if file or directory already exists
if [[ -f "${FSPATH}/sanctus_fs" || -d "${FSPATH}/sanctus_fs" ]]; then
  printf "Path already exists:\n ${FSPATH}/sanctus_fs\n"
  read -p "Override? [y/N]: " CONFIRM
  if [[ ${CONFIRM} != "y" ]]; then
    echo "Abandoned."
    exit 1;
  fi
fi

# Create filesystem's subdirectories by sha-1 hash
echo ""
rm -fr "${FSPATH}/sanctus_fs"
mkdir -p "${FSPATH}/sanctus_fs"
echo "${FSPATH}/sanctus_fs" >> sanctusenv

cd "${FSPATH}/sanctus_fs"

for i in {0..9}{a..f}; do
  mkdir ${i}
done

for i in {a..f}{0..9}; do
  mkdir ${i}
done

cd ..
chmod --recursive a+rwx "sanctus_fs"
export SANCTUS_FS="${FSPATH}/sanctus_fs"
echo "File storage created at: ${SANCTUS_FS}"
echo ""

exit 0;