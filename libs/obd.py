import obd

conn = obd.Async()
cmd = obd.commands


speed = cmd.SPEED
engine_load = cmd.ENGINE_LOAD
coolant_temp = cmd.COOLANT_TEMP
RPM = cmd.RPM
fuel_level = cmd.FUEL_LEVEL
ambient_air = cmd.AMBIENT_AIR_TEMP
oil_temp = cmd.OIL_TEMP
fuel_rate = cmd.FUEL_RATE
diagnostic_codes = cmd.GET_DTC
