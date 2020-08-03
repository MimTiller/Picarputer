import pygame

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
