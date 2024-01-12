#!/bin/bash

rm -f sanctusenv
cd install
rm -f sanctusenv
./create_fs.sh && ./init_db.sh

source sanctusenv

cd ../baseline
echo ""
bash "injection/000_composers.sh"
