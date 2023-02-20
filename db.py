import json
import uuid

import dataset
from flask import g

from app import *

"""
If it doesn't exist yet, Dataset will create a new file, database.db in this directory
Together with the database.db-shm and database.db-wal files
which are created on reads and writes (do not delete these!), it makes up the database
Open database.db with DB Browser for SQLite to inspect its contents
You can copy these three files somewhere to make a backup of your database
"""

DATABASE = "sqlite:///database.db?check_same_thread=False"

def get_table():
	"""can be called by any function to get access to the database table called 'saves'"""

	db = getattr(g, "_database", None)

	if db is None:
		db = g._database = dataset.connect(DATABASE)

	return db["saves"]

def save_json(j):
	"""creates a new row in the database. dataset will insert columns automatically if they don't exist yet
	the same goes for the table and the database file"""

	table = get_table()

	code = str(uuid.uuid4())

	row = {
		"code": code,
		"data": json.dumps(j)
	}

	table.insert(row)

	return code

def load_json(code):
	"""will return None if no row with that input"""

	table = get_table()

	result = table.find_one(code=code)

	if result is None:
		return None

	return json.loads(result["data"])

"""
Utility to execute requests interactively

$ python
>>> from db import *
>>> code = with_context(save_json, {'test': 123})
>>> code
'516a1030-eeec-43a4-b247-c5cf81690c91'
>>> with_context(load_json, code)
{'test': 123}
"""
def with_context(f, *args, **kwargs):
    with app.app_context():
        return f(*args, **kwargs)
