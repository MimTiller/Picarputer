import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='hide'
import pygame,os,sounddevice

def current_res():
	pygame.init()
	info = pygame.display.Info()
	current_res = str(info.current_w) + 'x' + str(info.current_h)
	return current_res

def supported_res():
	pygame.init()
	supported_res = []
	resolutions = pygame.display.list_modes()
	for x in resolutions:
		supported_res.append(str(x[0]) + 'x' + str(x[1]))
	return supported_res

def get_wallpapers():
	cwd = os.getcwd() + "\\data\\wallpapers"
	wallpaperlist = [f for f in os.listdir(cwd)]
	#self.ids.wpspinner.text = files[0]
	#print (files[0])
	#self.ids.wpspinner.bind(text = self.on_spinner_select)
	return wallpaperlist

def get_audio_out():
	sd = sounddevice
	device_list = []
	for device in sd.query_devices():
		if device['max_output_channels'] > 0:
			device_list.append(device['name'])
	return device_list

def sources():
	source_list = ['Spotify','Aux','Bluetooth','USB']
	return source_list
