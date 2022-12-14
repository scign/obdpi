import obd


class ObdManager:

    def __init__(self):
        self.obd_connection = None
        self.cmds = [cmd.name for mode in obd.commands for cmd in mode if cmd]

    def init_obd_connection(self, serial_connection_id):
        if obd.scan_serial():
            if serial_connection_id in obd.scan_serial():
                self.obd_connection = obd.OBD(serial_connection_id)

    def has_obd_connection(self):
        if self.obd_connection:
            if self.obd_connection.is_connected():
                return True
            else:
                return False
        else:
            return False

    def generate_obd_response(self, command):
        if not self.has_obd_connection():
            return "No OBD connection"
        
        if command not in self.cmds:
            return "'" + command + "' is unrecognized OBD command"

        obd_response = self.obd_connection.query(obd.commands[command])

        if obd_response.is_null():
            return "No OBD response"
        
        # converted_obd_response = round(obd_response.value * self.KPA_TO_PSI_CONVERSION_FACTOR, 3)
        # converted_obd_response = round(obd_response.value, 3)
        return str(obd_response) #(converted_obd_response)
            
