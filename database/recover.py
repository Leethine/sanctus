#/usr/bin/python3

import json, os, sqlite3

recovery_file_name = os.environ['FILENAME']
recovery_file_type = os.environ['FILETYPE']

conn = sqlite3.connect(os.environ['DBFILE'])
cursor = conn.cursor()

with open(recovery_file_name, 'r') as f:
  j  = json.load(f)
  ks = list(j[0].keys())
  for item in j:
    vals = []
    for k in ks:
      if item[k] is None:
        vals.append(f"null")
      elif type(item[k]) is str:
        vals.append(f"'{item[k]}'")
      elif type(item[k]) is int:
        vals.append(f"{item[k]}")
    rowkeys = ",".join(ks)
    rowvals = ",".join(vals)
    SQL = f"INSERT INTO {recovery_file_type} ({rowkeys}) VALUES({rowvals});"
    try:
      cursor.execute(SQL)
      conn.commit()
      #print(SQL+"\n")
    except sqlite3.Error as e:
      print(f"SQL Syntax Error: \n{e}\nThe SQL statement was:\n{SQL}")
      exit(1)
