"""
Created by Jordan Burton, 03/07/2017
"""
import os
import json
import shutil

totalData = []


def readFile(filename):
	file = open("../txt_files/" + filename)
	lines = []
	for line in file:
		line = line.strip().split()
		lines.append(line)
	file.close()
	artist = " ".join(lines[0])
	album =  " ".join(lines[1])
	year = ""
	lyrics = []
	try:

		year = int("".join(lines[2]))
		lyrics = lines[3:]
	except:
		lyrics = lines[2:]
	
	return artist, album, year, lyrics


def writeJsonSong(artist, album, filename, data):
	directory = '../' + artist + '/' + album + '/' + getSongTitle(filename, album, artist) + '.json'
	if not os.path.exists(os.path.dirname(directory)):
	    try:
	        os.makedirs(os.path.dirname(directory))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise
	with open(directory, 'w') as outfile:
		json.dump(data, outfile, indent=4, sort_keys=True)
	return 

def writeJsonTotal(data):
	directory = "../overall_data/data.json"
	with open(directory, 'w') as outfile:
		json.dump(data, outfile, indent=4, sort_keys=True)
	return

def writeLyrics(artist, album, filename):
	directory = '../' + artist + '/' + album + '/' + "lyrics/" + filename
	if not os.path.exists(os.path.dirname(directory)):
	    try:
	        os.makedirs(os.path.dirname(directory))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise
	shutil.copy("../txt_files/" + filename, directory)

def getUnique(lines):
	uniqueSet = set([])
	for line in lines:
		newSet = set(" ".join(line).replace("\n", " ").replace("!", "").replace("?", "").replace("(", "").replace(")", "").replace(".", "").replace("\"", "").split())
		uniqueSet = uniqueSet | newSet
	return (len(uniqueSet), list(uniqueSet))


def countEachWord(lyrics):
	lyrics = joinLyrics(lyrics)
	my_lyrics = lyrics.replace("!", "").replace("\n", " ").replace("?", "").replace("(", "").replace(")", "").replace(".", "").replace("\"", "")
	my_lyrics = my_lyrics.split()
	total = len(my_lyrics)
	my_word_counts = {}
	for word in my_lyrics:
		if(word not in my_word_counts):
			my_word_counts[word] = 0
		my_word_counts[word] += 1
	return (total, my_word_counts) 


def joinLyrics(lyrics):
	joined = ""
	for line in lyrics:
		joined += " ".join(line) + "\n"
	return joined

def getSongTitle(name, album, artist):
	filename = name.strip(".txt").replace(artist + " " + album + " ", "", 1)
	filename= filename.strip()
	return filename

def processData():
	directory = "../txt_files/"
	for filename in os.listdir(directory):
		songDict = {}
		if filename.endswith(".txt") or filename.endswith(".txt"):
			artist, album, year, lyrics = readFile(directory + filename)
			songDict["song_title"] = getSongTitle(filename, album, artist)
			songDict["lyrics"] = joinLyrics(lyrics)
			songDict['album'] = album
			songDict['year'] = year
			songDict["unique_words"] = getUnique(lyrics)
			songDict["total_words"] = countEachWord(lyrics)
	    		writeJsonSong(artist, album, filename.strip(".txt"), songDict)
	    		writeLyrics(artist, album, filename)
	    	if(songDict):
	    		totalData.append(songDict)
	writeJsonTotal(totalData)

def main():
	processData()


if __name__ == '__main__':
	main()
