from bluetooth import *

print ("checking available devices....")

nearby_devices = discover_device(lookup_names = True)
print ("found {} devices".format(len(nearby_devices)))
for name, addr in nearby_devices:
	print "{}--{}".format(addr,name)
