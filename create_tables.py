import sqlite3

with sqlite3.connect("tguser_lang.db") as connection:
    cursor = connection.cursor()

create_tguser_lang = ("""CREATE TABLE tguser_lang
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  tg_user_id VARCHAR (20) NOT NULL UNIQUE, 
  text_language VARCHAR (5) DEFAULT ('en'),
  src_language VARCHAR (9) DEFAULT ('auto'),
  wiki_enabled BOOLEAN DEFAULT (TRUE)
  )
  """)

cursor.execute(create_tguser_lang)

cursor.close()
