from datetime import datetime, timezone

time_now = datetime.now(timezone.utc).astimezone().isoformat()
with open('/home/aleem/test_file', 'a') as f:
    f.write(f"{time_now}\n")

import atexit
import sys
from time import sleep

import obdpi.shared_settings
from obdpi.log_manager import LogManager
from obdpi.serial_manager import SerialManager
from obdpi.obd_manager import ObdManager

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


def start(obd_command):
    while True:
        if init_serial(obdpi.shared_settings.is_testing, obdpi.shared_settings.environment) == "SUCCESS":
            if init_obd(ser_man.connection_id) == "SUCCESS":
                break
        sleep(1.0)
    while True:
        obd_response = get_obd_response(obd_command)
        sleep(0.15)


@log_man.log_event_decorator("Ending Script", "INFO")
def end():
    sys.exit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        obd_command = str(sys.argv[1])
    elif obdpi.shared_settings.obd_command is not None:
        obd_command = str(obdpi.shared_settings.obd_command)
    else:
        obd_command = "RPM"

    obd_command = "ENGINE_LOAD"

    atexit.register(end)
    with open('/home/aleem/test_file', 'a') as f:
        f.write(f"Start scanning\n")
    start(obd_command)
