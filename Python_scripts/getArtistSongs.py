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
proxyList = ['12.129.82.194:8080', '218.191.247.51:8380', '207.188.73.155:80', '180.211.193.66:8080'] #['162.213.213.159:80', '72.159.158.210:3128', '35.167.66.19:3128', '184.175.106.139:80', '198.71.88.16:443'] #, '123.30.238.16:3128', '97.77.104.22:80', '63.150.152.151:8080'] #'87.242.77.197:8080', '97.77.104.22:3128']

users = []
i = 0

editAlbums = ['Catastrophic', 'Catastrophic 2']
albumYears = [2012, 2014]
newYearsDict = {}

def getUsers():
	f = open('fakeUserList.txt', 'r')
	for line in f:
		line = line.strip()
		users.append(line)

def getEditAlbums():
	for (album, year) in zip(editAlbums, albumYears):
		newYearsDict[album] = str(year)

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

def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result

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
		FACTOR_TO_SLEEP = 100.0
		majorSeconds = random.randint(15, 40)
		minorSeconds = (1/FACTOR_TO_SLEEP) * random.randint(1, int(FACTOR_TO_SLEEP))
		totalSeconds = majorSeconds + minorSeconds
		time.sleep(totalSeconds)

	for x in albumList:
		info = x.strip("album: ").split("\n")
		albumInfo = re.sub(r'<.*?>', '', info[0]) #info[0].strip("</div>").replace("</b>", "").replace("<b>", "").replace('"', '').replace('b>', '')
		print albumInfo
		albumName = albumInfo.split('"')[1]
		if albumName != 'Catastrophic 2':
			continue
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
			
			try:
				sizeOfFile = os.path.getsize(fullName)
				if sizeOfFile > 100.0:
					print songName, "IS AT SIZE", sizeOfFile
					continue
			except:
				pass
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

def reMakeWithYear():
	getEditAlbums()
	for subdir, dirs, files in os.walk(toSaveBeginning):
		for f in files:
			for album in editAlbums:
				if album in f:
					print album
					dirLoc = subdir + f
					oldDoc = open(dirLoc, 'r')
					newName = dirLoc+"2"
					newSave = open(newName, 'w')
					i = 0
					for line in oldDoc:
						i += 1
						if i == 3:
							newSave.write(newYearsDict[album])
							newSave.write('\n')
							continue
						newSave.write(line)
					newSave.close()
					os.rename(newName, dirLoc)
					# os.remove(newName)
					break



def main():
	# artistName = raw_input("AZ Name")
	getUsers()
	# #getAlbums('Eminem')
	# readArtists('azMap.csv')
	getAlbums('Busta Rhymes', 'http://www.azlyrics.com/b/busta.html')
	return

if __name__ == '__main__':
	# main()
	reMakeWithYear()