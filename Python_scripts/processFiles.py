"""
Created by Jordan Burton, 03/07/2017
"""
import os
import json

totalData = {}


def readFile(filename):
	file = open("../txt_files/" + filename)
	lines = []
	for line in file:
		line = line.strip().split()
		lines.append(line)
	file.close()
	return " ".join(lines[0]), "_".join(lines[1]), lines[2:]


def writeJson(artist, album, filename, data):
	directory = '../' + artist + '/' + album + '/' + filename + '.json'
	if not os.path.exists(os.path.dirname(directory)):
	    try:
	        os.makedirs(os.path.dirname(directory))
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise
	with open(directory, 'w') as outfile:
		json.dump(data, outfile)
	return 


def getUnique(lines):
	uniqueSet = set([])
	for line in lines:
		newSet = set(line)
		uniqueSet = uniqueSet | newSet
	return (len(uniqueSet), list(uniqueSet))


def processData():
	directory = "../txt_files/"
	for filename in os.listdir(directory):
		songDict = {}
		if filename.endswith(".txt") or filename.endswith(".txt"):
			artist, album, lyrics = readFile(directory + filename)
			songDict["Unique"] = getUnique(lyrics)
	    		writeJson(artist, album, filename.strip(".txt"), songDict)

def main():
	processData()


if __name__ == '__main__':
	main()
