import sqlite3 as lite
import json
import sys
import os

def makeDB():
    con = lite.connect("RapMining.db")
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Albums")
        cur.execute("DROP TABLE IF EXISTS Songs")
        cur.execute("DROP TABLE IF EXISTS Words")
        cur.execute("CREATE TABLE Albums(ID INT, Name TEXT, Artist TEXT, Year INT)")
        cur.execute("CREATE TABLE Songs(ID INT, Name TEXT, Artist TEXT, Album TEXT, Lyrics TEXT, WordCount INT, UWordCount INT)")
        cur.execute("CREATE TABLE Words(Word TEXT, Freq INT)")  

def navigateDirectory():
    directory = "..\\test_files\\"
    albumIndex = 1
    songIndex = 1
    for artist in os.listdir(directory):
        dirArt = directory + artist + "/"
        for album in os.listdir(dirArt):
            dirAlb = dirArt + album + "/"
            addAlbum(albumIndex, album, artist, 2017)
            albumIndex += 1
            for song in os.listdir(dirAlb):
                songFile = dirAlb + song
                data = json.read(songFile)
                addSong(data, artist, album, song, index)
                songIndex += 1
                
def addSong(data, artist, album, song, index):
    total_words = data["total_words"][0]
    total_dict = data["total_words"][1]
    lyrics = data["lyrics"]
    unique_words = data["unique_words"][0]
    unique_dict = data["unique_words"][1]
    
    con = lite.connect("RapMining.db")
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Songs VALUES (%d, %s, %s, %s, %d, %d)" % (index, song, artist, album, lyrics, total_words, unique_words))
    
    addWords(total_dict)
    
def addWords(dict):
    con = lite.connect("RapMining.db")
    with con:
        cur = con.cursor()
        for word in dict:
            cur.execute("SELECT * FROM Words WHERE Word = %s" % word)
            result = cur.fetchall()
            if not result:
                cur.execute("INSERT INTO Words VALUES (%s, %d)" % (word,dict[word]))
            else:
                newCount = result[0]["Freq"] + dict[word]
                cur.execute("UPDATE Words SET Freq = %d WHERE Word = %s" % (newCount, word))

        
def addAlbum(index, name, artist, year):
    con = lite.connect("RapMining.db")
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Albums VALUES (%d, %s, %s, %d)" % (index, name, artist, year))
        

if __name__ == '__main__':
    makeDB()
    navigateDirectory()
    