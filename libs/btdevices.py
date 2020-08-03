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

def bt_song_info(interface, changed, invalidated):
    if interface != 'org.bluez.MediaPlayer1':
        return
    for prop, value in changed.items():
        if prop == 'Status':
            print('Playback Status: {}'.format(value))
        elif prop == 'Track':
            print('Music Info:')
            for key in ('Title', 'Artist', 'Album'):
                print('   {}: {}'.format(key, value.get(key, '')))

def bluetooth_control(fd,condition):
    str = fd.readline()
    if str.startswith('play'):
        player_iface.Play()
    elif str.startswith('pause'):
        player_iface.Pause()
    elif str.startswith('next'):
        player_iface.Next()
    elif str.startswith('prev'):
        player_iface.Previous()
    elif str.startswith('vol'):
        vol = int(str.split()[1])
        if vol not in range(0, 128):
            print('Possible Values: 0-127')
            return True
        transport_prop_iface.Set(
                'org.bluez.MediaTransport1',
                'Volume',
                dbus.UInt16(vol))
    return True
