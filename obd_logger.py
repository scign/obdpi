from datetime import datetime, timezone

time_now = datetime.now(timezone.utc).astimezone().isoformat()
with open('/home/aleem/test_file', 'a') as f:
    f.write(f"{time_now}\n")

import atexit
import sys
from time import sleep

import obdpi.shared_settings as SETTINGS
from obdpi.log_manager import LogManager
from obdpi.serial_manager import SerialManager
from obdpi.obd_manager import ObdManager

import obd

log_man = LogManager()
ser_man = SerialManager()
obd_man = ObdManager()


@log_man.log_event_decorator("Initialize Serial Connection", "INFO")
def init_serial(is_testing, environment):
    try:
        ser_man.init_serial_connection(is_testing, environment)
        if ser_man.has_serial_connection():
            return "SUCCESS"
        else:
            return "FAIL"
    except Exception as e:
        return "[EXCEPTION] " + str(e)


@log_man.log_event_decorator("Initialize OBD Connection", "INFO")
def init_obd(connection_id):
    try:
        obd_man.init_obd_connection(connection_id)
        if obd_man.has_obd_connection():
            return "SUCCESS"
        else:
            return "FAIL"
    except Exception as e:
        return "[EXCEPTION] " + str(e)


@log_man.log_event_decorator("OBD Response", "INFO")
def get_obd_response(obd_command):
    try:
        obd_response = str(obd_man.generate_obd_response(obd_command))
        return obd_response
    except Exception as e:
        return "[EXCEPTION] " + str(e)


def start():
    obd_connected = False
    try_counter = SETTINGS.serial_attempt_count
    
    while try_counter:
        if init_serial(SETTINGS.is_testing, SETTINGS.environment) == "SUCCESS":
            if init_obd(ser_man.connection_id) == "SUCCESS":
                obd_connected = True
                break
        sleep(SETTINGS.serial_repeat_delay)
        try_counter -= 1
    
    if not obd_connected:
        timeout = SETTINGS.serial_repeat_delay * SETTINGS.serial_attempt_count
        log_man.add_warning_entry_to_log(f"OBD connection was not detected within {timeout} seconds")
        end()

    # loop over all commands
    for cmd in obd_man.cmds:
        get_obd_response(cmd)
    

@log_man.log_event_decorator("Ending Script", "INFO")
def end():
    sys.exit()


if __name__ == "__main__":
    atexit.register(end)
    with open('/home/aleem/test_file', 'a') as f:
        f.write(f"Start scanning\n")
    start()
