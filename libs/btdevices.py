import bluetooth, time

def get_bluetooth_devices():
	print ("checking available devices....")
	nearby_devices = bluetooth.discover_devices(lookup_names = True)
	print ("found {} devices".format(len(nearby_devices)))
	bluetooth_list = []
	for name, addr in nearby_devices:
		bluetooth_list.append("{}--{}".format(addr,name))
	if bluetooth_list == []:
		return ["None"]
	else:
		return bluetooth_list

def bluetooth_search():
	pass

def bluetooth_connect():
	pass
