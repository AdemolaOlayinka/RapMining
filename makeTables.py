import sqlite3 as lite
import sys

con = lite.connect("RapMining.db")

with con:
    
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Albums")
    cur.execute("DROP TABLE IF EXISTS Songs")
    cur.execute("DROP TABLE IF EXISTS Words")
    cur.execute("CREATE TABLE Albums(ID INT, Name TEXT, Artist TEXT, Year INT)")
    cur.execute("CREATE TABLE Songs(ID INT, Name TEXT, Album TEXT, Lyrics TEXT)")
    cur.execute("CREATE TABLE Words(ID INT, Word TEXT, Freq INT)")
    cur.execute("INSERT INTO Albums VALUES(1, 'The Marshall Mathers LP', 'Eminem', 2000)")
    cur.execute("INSERT INTO Songs VALUES(1, 'The Real Slim Shady', 'The Marshall Mathers LP', 'Y''all act like...')")
    