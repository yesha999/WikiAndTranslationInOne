import sqlite3

with sqlite3.connect("tguser_lang.db") as connection:
    cursor = connection.cursor()

create_tguser_lang = ("""CREATE TABLE tguser_lang
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  tg_user_id VARCHAR (20) NOT NULL UNIQUE, 
  text_language VARCHAR (2) DEFAULT ('en'),
  wiki_enabled BOOLEAN DEFAULT (TRUE)
  )
  """)

cursor.execute(create_tguser_lang)

cursor.close()


