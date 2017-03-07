"""
Created by Jordan Burton, 03/07/2017
"""

def readFile(filename):
	file = open(filename)
	lines = []
	for line in file:
		line = line.strip()
		lines.append(line)
	return lines


print readFile("../ListOfArtists.txt")