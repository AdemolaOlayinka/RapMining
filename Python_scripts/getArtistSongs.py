'''
@Author: Ademola Olayinka
Created: 2017 March 7
'''

from lxml import html
from Queue import *
import requests
import time
import re
import os, sys
import random
import csv

BEGINNING_URL = "http://www.azlyrics.com/"
headers = { 'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11' }
toSaveBeginning = "../txt_files/"
proxyList = ['96.239.193.243:8080', '66.254.177.146:3128', '74.62.65.82:8080', '40.138.64.36:8080', '206.128.191.77:8008', '104.236.48.178:8080', '130.211.112.215:80']#['162.213.213.159:80', '72.159.158.210:3128', '35.167.66.19:3128', '184.175.106.139:80', '198.71.88.16:443'] #, '123.30.238.16:3128', '97.77.104.22:80', '63.150.152.151:8080'] #'87.242.77.197:8080', '97.77.104.22:3128']

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
	#print fakeProxy
	i += 1
	return {'http': fakeProxy}


def writeToFile(artistName, songName, albumName, lyrics, year):
	fileName = artistName + ' ' + albumName + ' ' + songName
	fileName = fileName.replace('/', '').replace('.', '')
	fileName += '.txt'
	file = open(toSaveBeginning + fileName, 'w')
	file.write(artistName)
	file.write('\n')
	file.write(albumName)
	file.write('\n')
	file.write(str(year))
	file.write('\n')
	file.write(lyrics.strip().replace('\n\n', '\n'))
	file.close()

def getLyrics(songURL, artistURL):
	
	if songURL.startswith('..'):
		end = songURL[2:]
		songURL = BEGINNING_URL + end
		# print songURL
	try:
		songPage = requests.get(songURL, headers=makeRandomUser(), proxies=getRandomProxy())
	except requests.exceptions.ConnectionError:
		return ''
	# print songPage.content
	tree = html.fromstring(songPage.content)
	lyrics = tree.xpath('//div[not(@id) and not(@class)]/text()')
	
	# print lyrics
	return u''.join(lyrics).encode('utf-8').strip()


def getAlbums(artistName, fullURL):
	#name is the url based name
	songWaitQueue = Queue() #songs which failed are added here
	try:
		artistPage = requests.get(fullURL, headers=makeRandomUser(), proxies=getRandomProxy())
	except requests.exceptions.ConnectionError:
		return False
	htmlString = artistPage.content
	albumList = htmlString.split('<div class="album">')[1:-1]

	if len(albumList) == 0:
		#in case of access forbidden
		return False #on failure

	def addSong(sURL, sName, aName, aYear):
		#s is short for song
		#a is for album
		songLyrics = getLyrics(sURL, sName)
		if len(songLyrics) == 0:
			songWaitQueue.put((sURL, sName, aName, aYear)) #parameters of function are added
			print "SONG", songName, "FAILED. ADDED TO QUEUE AND MOVING ON"
			return
		#print "LYRICS"
		#print songLyrics
		writeToFile(artistName, sName, aName, songLyrics, aYear)
		print "Wrote song", songName
		time.sleep(random.randint(3, 7))

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

			#THIS PART SHOULD BE COMMENTED OUT WHEN REWORKING
			#ONLY FOR USE TO PREVENT REREADING
			fileName = artistName + ' ' + albumName + ' ' + songName
			fileName = fileName.replace('/', '').replace('.', '')
			fileName += '.txt'
			fullName = toSaveBeginning + fileName
			if os.path.exists(fullName):
				continue
			#CLOSE THE PART WHICH ASKS FOR THIS

			addSong(songURL, songName, albumName, albumYear)
		print

	while (not songWaitQueue.empty()):
		#songs which had their requests denied will try again
		songURL, songName, albumName, albumYear = songWaitQueue.get()
		addSong(songURL, songName, albumName, albumYear)
	print
	# tree = html.fromstring(artistPage.content)

	# albums = tree.xpath('//div[@class="album"]/b/text()')
	# print [x.strip('"') for x in albums]

	return True #on success

def readArtists(filename):
	#gets the CSV file and reads the artists
	f = open(filename, 'r')
	reader = csv.DictReader(f)
	artistWaitQueue = Queue()

	for row in reader:
		artistName = row['Artist Name']
		artistURL = row['AZ Lyrics URL']
		print
		print artistName
		if len(artistURL) == 0:
			print artistName, "is likely done or does not have a url"
			continue
		if (not getAlbums(artistName, artistURL)):
			print "ARTIST", artistName, "FAILED. ADDED TO QUEUE"
			artistWaitQueue.put((artistName, artistURL))
	while(not artistWaitQueue.empty()):
		artistName, artistURL = artistWaitQueue.get()
		if (not getAlbums(artistName, artistURL)):
			print "ARTIST", artistName, "FAILED. RE-ADDED TO QUEUE"
			artistWaitQueue.put((artistName, artistURL))

def main():
	# artistName = raw_input("AZ Name")
	getUsers()
	#getAlbums('Eminem')
	readArtists('azMap.csv')
	return

if __name__ == '__main__':
	main()