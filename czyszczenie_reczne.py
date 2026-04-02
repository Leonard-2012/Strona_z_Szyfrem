import sqlite3 as sql3

conn = sql3.connect('datas/aktywne.db')
cur = conn.cursor()
cur.execute("DELETE FROM aktywne_slowa")
conn.commit()
conn.close()