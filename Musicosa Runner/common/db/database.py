from os import path, getenv

from peewee import SqliteDatabase, OperationalError

db_path = getenv('MUSICOSA_DB_PATH', '')

if not path.isfile(db_path):
    print(f"[DB ERROR] Database not found at '{db_path}'")
    exit(1)

db = SqliteDatabase(db_path, pragmas={"foreign_keys": 1})

try:
    db.connect()
except OperationalError as err:
    print(f"[DB ERROR] Error connecting to database: {err}")
    exit(1)
