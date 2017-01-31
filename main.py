from __future__ import unicode_literals
from bs4 import BeautifulSoup
import youtube_dl
import urllib2
import urllib
import os

def downloadSong(song_string):
	print 'Currently Playing: ' + song_string
	print 'Downloading now...'

	query = urllib.quote(song_string)
	response = urllib2.urlopen("https://www.youtube.com/results?search_query=" + query)
	soup = BeautifulSoup(response.read(), "lxml")

	url = 'https://www.youtube.com' + soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]['href']
	
	ydl_opts = {
	'format': 'bestaudio/best',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
	'outtmpl': 'songs/%(title)s.%(ext)s'
	}
	
	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
	except:
		print "Error downloading song from YouTube, try running the script again or updating youtube_dl."

if os.name == 'nt':
	import spotilib
	
	if spotilib.song() == "There is nothing playing at this moment":
		print spotilib.song()
	else:
		song_string = spotilib.song() + ' by ' + spotilib.artist()
		downloadSong(song_string)

else:
	import applescript
	
	scpt = applescript.AppleScript('''
	set currentlyPlayingTrack to getCurrentlyPlayingTrack()
	on getCurrentlyPlayingTrack()
	tell application "Spotify"
	    set currentArtist to artist of current track as string
	    set currentTrack to name of current track as string
	
	    return currentTrack & " by " & currentArtist
	end tell
	end getCurrentlyPlayingTrack
	''')
	
	try:
		song_string = str(scpt.run())
		downloadSong(song_string)
		
	except:
		print "There is nothing playing at this moment"