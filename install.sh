#!/bin/bash

# Customize path to store the data
if [[ -z ${SANCTUS_DATAPATH} ]]; then
  echo "env variable SANCTUS_DATAPATH not set"
fi

cp database/schema.sql ${SANCTUS_DATAPATH}

database/init-db.sh

echo ""
echo "Installation done."
