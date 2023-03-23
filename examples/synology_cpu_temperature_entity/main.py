from reacthass import Reactor
from synology_api import core_sys_info
from time import sleep

# Synology settings
username = 'username'
password = 'password'
syno_url = 'synology url'
syno_port = 'port'

# Initiate synology session
syno = core_sys_info.SysInfo(syno_url, syno_port, username, password, True)

# reacthass settings
token = 'YOUR TOKEN'
hassurl = 'HOME ASSISTANT URL'

# Initiate reacthass session
hass = Reactor(hassurl, token, verify_ssl=False)


def main():
    while True:
        syno_temp = syno.get_cpu_temp()  # get synology cpu temperature
        hass.send_value_to_entity('sensor.synology_cpu_temperature_python', syno_temp, attributes={})
        sleep(30)  # sleep to avoid making too many requests


if __name__ == '__main__':
    main()
