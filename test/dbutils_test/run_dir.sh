#!/bin/bash

for fn in $(ls 0*.py); do
  python ${fn}
done