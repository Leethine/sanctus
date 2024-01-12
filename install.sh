#!/bin/bash

rm -f sanctusenv
cd install
rm -f sanctusenv
./create_fs.sh && ./init_db.sh

cd ../baseline
echo ""
bash "injection/000_composers.sh"