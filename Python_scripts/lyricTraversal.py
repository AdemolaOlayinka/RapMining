import os
from gensim import corpora, models, similarities
from operator import itemgetter

songList = []

def findLyrics():
    rootDir = 'Artists'
    count = 0
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname.endswith(".txt"):
                fullPath = dirName + "/" + fname
                with open(fullPath, 'r') as song:
                    songList.append("")
                    skip = 0
                    for line in song:
                        skip+= 1
                        if skip < 4: #to ignore header thats not lyrics
                            continue
                        songList[count] += " " + line.strip("\n")
                    count += 1
 

def calcScores(songList):
    lyrics = [[word.strip(",:;.?!") for word in document.lower().split()] for document in songList]
    dictionary = corpora.Dictionary(lyrics)
    corpus = [dictionary.doc2bow(text) for text in lyrics]
    tfidf = models.TfidfModel(corpus)
    tfidfList = list()
    for each in corpus:
        tfidfList.append(tfidf[each])
    sortScore(tfidfList, dictionary)

def sortScore(tfidfList, dictionary):
    for i in range(len(tfidfList)):
        local3 = list()
        top3 = sorted(tfidfList[i], key = itemgetter(1), reverse=True)[:3]
        for word in top3:
            local3.append(dictionary[word[0]])
            print(dictionary[word[0]])

findLyrics()
calcScores(songList)
