from libs import spotify
import urllib

def control_playback(control_msg,source):
		track = get_track_info(source)
		is_playing = track['is_playing']
		shuffle_state = track['shuffle_state']
		if control_msg == 'playpause':
			if is_playing == True:
				control_msg = 'pause'
			else:
				control_msg = 'play'
		if control_msg == 'shuffle':
			if shuffle_state == True:
				control_msg = 'shuffle_off'
			else:
				control_msg = 'shuffle_on'
		if isinstance(control_msg,float):
			control_msg = int(control_msg)
		print('(Spotify.py) sending {} command'.format(control_msg))
		spotify.control(control_msg)


def get_track_info(source):
	if source == 'Spotify':
		track = spotify.get_playing()
		return track

	elif source == 'USB':
		pass
	elif source == 'Bluetooth':
		pass

def get_album_art(source,track):
	if source == 'Spotify':
		art = track['art']
		albumart = urllib.request.urlretrieve(art,'temp.png')
		return 'temp.png'
