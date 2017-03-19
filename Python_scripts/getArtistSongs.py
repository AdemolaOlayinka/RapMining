'''
@Author: Ademola Olayinka
Created: 2017 March 7
'''

from lxml import html
import requests
import time
import re
import os, sys
import random

BEGINNING_URL = "http://www.azlyrics.com/"
headers = { 'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11' }
toSaveBeginning = "../txt_files/"
proxyList = ['165.234.102.177:8080'] #, '123.30.238.16:3128', '97.77.104.22:80', '63.150.152.151:8080'] #'87.242.77.197:8080', '97.77.104.22:3128']

users = []
i = 0

def getUsers():
	f = open('fakeUserList.txt', 'r')
	for line in f:
		line = line.strip()
		users.append(line)

def makeRandomUser():
	fakeUser = random.choice(users)
	return {'User-Agent': fakeUser}

def getRandomProxy():
	global i
	fakeProxy = proxyList[i%len(proxyList)]
	i += 1
	return {'http': fakeProxy}


def writeToFile(artistName, songName, albumName, lyrics, year):
	fileName = artistName + ' ' + albumName + ' ' + songName + ".txt"
	fileName = fileName.replace('/', '')
	file = open(toSaveBeginning + fileName, 'w')
	file.write(artistName)
	file.write('\n')
	file.write(albumName)
	file.write('\n')
	file.write(str(year))
	file.write('\n')
	file.write(lyrics.strip().replace('\n\n', '\n'))
	file.close()

def getLyrics(songURL):
	
	songPage = requests.get(songURL, headers=makeRandomUser(), proxies=getRandomProxy())
	# print songPage.content
	tree = html.fromstring(songPage.content)
	lyrics = tree.xpath('//div[not(@id) and not(@class)]/text()')
	
	# print lyrics
	return u''.join(lyrics).encode('utf-8').strip()


def getAlbums(artistName):
	#name is the url based name
	firstLetter = artistName[0].lower()
	fullURL = BEGINNING_URL + firstLetter + artistName.lower() + ".html"

	fullURL = "http://people.duke.edu/~aoo12/datamining/EMINEMlyrics.html"

	artistPage = requests.get(fullURL, headers=makeRandomUser())
	htmlString = artistPage.content
	albumList = htmlString.split('<div class="album">')[1:-1]

	for x in albumList:
		info = x.strip("album: ").split("\n")
		albumInfo = re.sub(r'<.*?>', '', info[0]) #info[0].strip("</div>").replace("</b>", "").replace("<b>", "").replace('"', '').replace('b>', '')
		print albumInfo
		albumName = albumInfo.split('"')[1]
		print "Starting print of", albumName
		albumYear = albumInfo.split('(')[-1][:-1]
		for y in info[1:-2]:
			songURL = y.split('"')[1]
			songName = re.sub(r'<.*?>', '', y)
			songLyrics = getLyrics(songURL)
			#print "LYRICS"
			#print songLyrics
			writeToFile(artistName, songName, albumName, songLyrics, albumYear)
			print "Wrote song", songName
			time.sleep(60)

		print
		print
	print
	tree = html.fromstring(artistPage.content)

	albums = tree.xpath('//div[@class="album"]/b/text()')
	print [x.strip('"') for x in albums]

def main():
	# artistName = raw_input("AZ Name")
	getUsers()
	getAlbums('Eminem')
	return

if __name__ == '__main__':
	main()