from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
import os, re, dataset

db = dataset.connect('sqlite:///songlist.db')
table = db['songs']
filelist = {".mp3":MP3, ".m4a":MP4, ".flac":FLAC}
memtable=[]

def filetagger(root,filename):
	location = os.path.join(root,filename)								#add the file together from filesearcher
	MP3KEYS = ['TIT2', 'TPE1', 'TALB', 'TRCK'] 						
	MP4KEYS =['\xa9nam','\xa9ART','\xa9alb','trkn']
	FLACKEYS= ['title', 'artist','album','tracknumber']														
	infolist = []
	title=''
	artist=''
	album=''
	keylist = {MP3:MP3KEYS, MP4:MP4KEYS, FLAC:FLACKEYS}
	
	for x in filelist:
		if filename.endswith(x):
			audio = filelist[x](location)
			for y in keylist[filelist[x]]:
				if audio.has_key(y):
					if filename.endswith('.mp3' or '.flac'):
						infolist.append(unicode(audio[y]))
					else:
						infolist.append(unicode(audio[y][0]))
				else:
					infolist.append('')

														
	location = unicode(location)									
	title = infolist[0]										
	if title == '':
		title = unicode(filename)
	artist = infolist[1]
	if artist == '':
		artist = 'Unknown'
	album = infolist[2]
	if album == '':
		album = 'Unknown'
	track = infolist[3]
	if track == '':
		track = '1'
	length = int(audio.info.length)										#get length in seconds
	size = round(os.path.getsize(location)/(1024*1024.0),1) 			#get size of file in MB rounded to 1 decimal
	try:
		bitrate = int(audio.info.bitrate/1000) 							#get bitrate of audio file
	except:
		bitrate = int((size/audiolength) * 10000)						#if no bitrate, divide file size by length to get bitrate
	track = re.sub(r'[\[\]\[()u\'|]', '', "".join(track.split()))		#take out unneccesary [ ] ( ) and extra spaces
	track = re.sub('-|,|\/', '-', track)								#replace , and / with -	
	track = track.split('-', 1)[0]

	for x in table.find(location=location):
		memtable.append(x['location'])
		if os.path.isfile(x['location']):
			pass
		else:
			db_adder(artist,album,title,track,size,length,bitrate,location)
			albumart(location)
def albumart(song):
	for x in table.find(location = song):
		album = x['album']
	album_img = "artwork/" + album + ".jpg"
	artkey = {MP3:'APIC:',MP4:'covr',FLAC:'cover'}
	
	for x in filelist:
		if song.endswith(x):
			audio = filelist[x](song)
			try:
				artwork = audio.tags[artkey[filelist[x]]].data
				with open(album_img, 'wb') as img:
					img.write(artwork)
					table.upsert(dict(location=song,albumart=album_img),['location'])
			except Exception as x:
				print 'Error:', x, song
				
	
def db_adder(artist,album,title,track,size,length,bitrate,location):
	print "adding", title
	table.insert(dict(artist = artist, album = album,title = title, track = track, size = str(size) + "MB", length = length, bitrate = str(bitrate) + "Kbps", location = location))
	
