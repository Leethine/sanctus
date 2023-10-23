#!/bin/bash

# Testing only, not in production 

#rm -fr $HOME/Music/dbtest/sanctus_db
#cp -r sanctus_db $HOME/Music/dbtest

mkdir -p $HOME/.local/lib/sanctus
rm -fr $HOME/.local/lib/sanctus/baseline
cp -r baseline $HOME/.local/lib/sanctus

cp -f sanctus $HOME/.local/bin