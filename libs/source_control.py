from libs.spotify import Spotify_ctrl
import urllib

def control_playback(control_msg,source,login):
		track = get_track_info(source,login)
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
		print('(source_control.py) sending {} command'.format(control_msg))
		Spotify_ctrl.control(control_msg,login)


def get_track_info(source,login="N/A"):
	if source == 'Spotify':
		sp = Spotify_ctrl()
		track = sp.get_playing(login)
		return track

	elif source == 'USB':
		pass
	elif source == 'Bluetooth':
		pass

def get_album_art(source,track):
	if source == 'Spotify':
		art = track['art']
		if art != None:
			albumart = urllib.request.urlretrieve(art,'temp.png')
			return 'temp.png'
		else:
			return 'unknown.png'
