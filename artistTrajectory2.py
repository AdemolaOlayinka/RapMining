#organized by: artist, album, songs (also lyrics file to ignore)

import json
import os
from collections import OrderedDict
import gensim
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models, similarities
from operator import itemgetter



artistDict = OrderedDict() #artist name to album name, album name to lyrics in song
lyricsDict = dict()

def findSong():
      rootDir = "./"
      for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname.endswith(".json"):
                fullPath = dirName + "/" + fname
                with open(fullPath, 'r') as data:
                    jsonF = json.load(data)
                    artist= jsonF["artist"]
                    lyrics = jsonF["lyrics"]
                    year = jsonF["year"]
                    info = []
                    if artist not in artistDict:
                        artistDict[artist] = dict()
                    if year not in artistDict[artist]:
                        artistDict[artist][year] = ""
                    artistDict[artist][year] += lyrics + " "

def salient():
  with open("artistSalient.txt", "w") as out, open("artistSalient.csv", "w") as csv:
    for artist in artistDict:
        for year in sorted(artistDict[artist]):
            sublist = []
            for word in artistDict[artist][year].lower().split():
                wrd = word.strip(",:;.?![]{}()").strip('""').strip("'") 
                if wrd not in STOPWORDS:
                    sublist.append(wrd)
            if artist not in lyricsDict:
                lyricsDict[artist] = []
            lyricsDict[artist].append(sublist)
    for artist in artistDict:
        if artist == "Ice Cube" or artist == "Grand Master Flash":
            continue
        years = sorted(artistDict[artist])
        dictionary = corpora.Dictionary(lyricsDict[artist])
        corpus = [dictionary.doc2bow(text) for text in lyricsDict[artist]]
        x = 2
        tfidf = models.TfidfModel(corpus)
        tfidfList = list()
        for each in corpus:
            tfidfList.append(tfidf[each])
        for i in range(len(tfidfList)):
            if artist == "Tyler, the Creator":
                artist = "Tyler the Creator"
            out.write(artist + ": ")
            csv.write(artist + ",")
            top10 = sorted(tfidfList[i], key = itemgetter(1), reverse=True)[:10]
            out.write(str(years[i]) + ": ")
            csv.write(str(years[i]) + ",")
            for i, word in enumerate(top10):
                out.write(dictionary[word[0]] + " " + str(word[1]) + " ")
                csv.write(dictionary[word[0]] + " " + str(word[1]))
                if i != 9:
                    csv.write(",")
            out.write("\n")
            csv.write("\n")
        out.write("\n")



findSong()
salient()

#albums