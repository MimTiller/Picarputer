import json

json_settings = json.dumps([
	{'type': 'numeric',
	'title': 'Startup Volume',
	'desc': 'Set the default startup volume for the picarputer',
	'key': 'startupvolume',
	'section': 'General'},
	{'type': 'dynamic_options',
	'title': 'options that are always up to date',
	'desc': 'List all compatible Bluetooth devices',
	'section': 'General',
	'key': 'bluetooth_list',
	'function_string': 'main.MainThread.get_bluetooth_devices()'
	}
	])
