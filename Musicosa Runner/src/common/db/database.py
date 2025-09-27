from os import getenv, path

from peewee import OperationalError, SqliteDatabase

db_path = getenv("DB_PATH", "")

if not path.isfile(db_path):
    print(f"[DB ERROR] Database not found at '{db_path}'")
    exit(1)

db = SqliteDatabase(db_path, pragmas={"foreign_keys": 1})

try:
    db.connect()
except OperationalError as err:
    print(f"[DB ERROR] Could not connect to database. Cause: {err}")
    exit(1)
