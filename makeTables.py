import sqlite3 as lite
import json
import sys

def makeDB():
    con = lite.connect("RapMining.db")
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Albums")
        cur.execute("DROP TABLE IF EXISTS Songs")
        cur.execute("DROP TABLE IF EXISTS Words")
        cur.execute("CREATE TABLE Albums(ID INT, Name TEXT, Artist TEXT, Year INT)")
        cur.execute("CREATE TABLE Songs(ID INT, Name TEXT, Album TEXT, Lyrics TEXT)")
        cur.execute("CREATE TABLE Words(ID INT, Word TEXT, Freq INT)")  

def navigateDirectory():
    directory = "../txt_files/"
    for artist in os.listdir(directory):
        dirArt = directory + artist + "/"
        for album in os.listdir(dirArt):
            dirAlb = dirArt + album + "/"
            for song in os.listdir(dirAlb):
                songFile = dirAlb+song
                data = json.lead(songFile)
                addValues(data, artist, album, song)
                
def addValues(data, artist, album, song):
    total_words = data["total_words"][0]
    total_dict = data["total_words"][1]
    lyrics = data["lyrics"]
    unique_words = data["unique_words"][0]
    unique_dict = data["unique_words"][1]
    

if __name__ == '__main__':
    makeDB()
    