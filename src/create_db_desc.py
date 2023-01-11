#!/usr/bin/python3
import json
import os, sys

usage_guide = """
create_db_desc.py
Create database descriptor json file.

Usage: 
  create_db_desc.py $pathtofile $rootpath
"""

if len(sys.argv) != 3:
  print(usage_guide)
else:
  json_template = json.dumps({"parent": "PARENT_DIR","children": "LIST_CHILD_DIR","cwd": "PWD_DIR"})

  parent_dir = ""
  list_child_dir = ""
  root_dir = os.path.abspath(str(sys.argv[2]))

  cd_dir = str(sys.argv[1])

  os.chdir(cd_dir)

  parent_dir = os.path.dirname(os.getcwd()).split("/")[-1]
  if root_dir == os.getcwd():
    parent_dir = "."
  else:
    parent_dir = os.path.dirname(os.getcwd()).split("/")[-1]

  pwd_dir = os.getcwd().replace(root_dir, "$ROOT")

  list_child_dir = str([f.name for f in os.scandir() if f.is_dir()])

  new_json = json_template.replace("PARENT_DIR", parent_dir).replace("LIST_CHILD_DIR", list_child_dir).replace("PWD_DIR", pwd_dir)

  # prettify
  new_json = json.loads(new_json)

  with open("_desc.json", "w") as jf:
    json.dump(new_json, jf, indent=2)
  