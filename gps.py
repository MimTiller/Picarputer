def gps_initiate(self):	
	import serial, os
	port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=10.0)

	line = []
	print("connected to: " + port.portstr)

	while True:
		try:
			rcv = port.readline()
		except:
			rcv = ''

		GPSDATA = []
		if "$GPRMC" in rcv:
			for x in rcv.split(','):
				GPSDATA.append(x)
			Latitude = GPSDATA[3].split('.')
			try:
				LaDegrees = float(Latitude[0][0:2])
				LaMinutes = float(Latitude[0][-2:])/60
				LaSeconds = float(str('.') + Latitude[1])/60
				Latitude = LaDegrees + LaMinutes + LaSeconds 
			except:
				pass
			if GPSDATA[3]=='S':
				Latitude = Latitude * -1
			try:
				Longitude = GPSDATA[5].split('.')
				LoDegrees = float(Longitude[0][0:3])
				LoMinutes = float(Longitude[0][-2:])/60
				LoSeconds = float(str('.') + Longitude[1])/60
				Longitude = LoDegrees + LoMinutes + LoSeconds
			except:
				pass
			if GPSDATA[6]=='W':
				Longitude = Longitude * -1

			Speed = float(GPSDATA[7]) * 1.15078
			Speed = round(Speed,2)
			Latitude_Direction = GPSDATA[4]
			Longitude_Direction = GPSDATA[6]	
			self.latitude = Latitude
			self.longitude = Longitude
			self.speed = Speed

		if "GPGGA" in rcv:
			for x in rcv.split(','):
				GPSDATA.append(x)
			Satellites = GPSDATA[7]
			self.satellites = Satellites
		try:
			self.ids.mapmarker.lat = Latitude
			self.ids.mapmarker.lon = Longitude
			self.ids.latitude.text = str(Latitude)
			self.ids.longitude.text = str(Longitude)
			self.ids.speed.text = str(Speed)
			self.ids.satellites.text = str(Satellites)

		except:
			pass
