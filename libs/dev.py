import bluetooth

mac = "94:8B:C1:F6:3F:AD"


def connect (btaddr):
    port = 2
    sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print("Trying to pair to", btaddr)
    sock.connect((btaddr, port))
    a = "a"
    while a != 'quit':
        a = input("<<< ")
        sock.send(a)
    sock.close()

def connect_l2cap(btaddr):
	sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)
	print("Trying to pair to", btaddr)
	sock.connect((btaddr, port))
	a = "a"
	while a != 'quit':
		a = input("<<< ")
		sock.send(a)
	sock.close()


def discover_services():
	sock=bluetooth.find_service(name=None, uuid=None)
	for x in sock:
		print (x)
connect_l2cap(mac)
