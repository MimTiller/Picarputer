import bluetooth, time



def bluetooth_search():

	print ("checking available devices....")
	nearby_devices = bluetooth.discover_devices(lookup_names = True)
	print ("found {} devices".format(len(nearby_devices)))
	bluetooth_list = []
	for name, addr in nearby_devices:
		bluetooth_list.append("{}--{}".format(addr,name))
	if bluetooth_list == []:
		print ("No Devices Found")
	return bluetooth_list
