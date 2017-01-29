from __future__ import unicode_literals
from bs4 import BeautifulSoup
import youtube_dl
import spotilib
import urllib2
import urllib

ydl_opts = {
	'format': 'bestaudio/best',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
	'outtmpl': 'songs/%(title)s.%(ext)s'
}

if spotilib.song() == "There is noting playing at this moment":
	print spotilib.song()
else:
	song_string = spotilib.song() + ' by ' + spotilib.artist()
	print 'Currently Playing: ' + song_string
	print 'Downloading now...'

	query = urllib.quote(song_string)
	response = urllib2.urlopen("https://www.youtube.com/results?search_query=" + query)
	soup = BeautifulSoup(response.read(), "lxml")

	url = 'https://www.youtube.com' + soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]['href']

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download([url])