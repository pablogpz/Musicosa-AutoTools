import Database from 'better-sqlite3'
import { sql } from 'drizzle-orm'
import { drizzle } from 'drizzle-orm/better-sqlite3'

const db = drizzle(new Database(process.env.DB_PATH))
db.run(sql`PRAGMA foreign_keys = ON`)

export default db