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

fan_domain = hass.get_domain('fan')  # get the fan domain


def main():
    while True:
        syno_temp = syno.get_cpu_temp()  # get synology cpu temperature
        if syno_temp >= '50':
            fan_domain.call_service('turn_on', 'fan.cooling_fan')  # turn on fan in the cabinet
        elif syno_temp <= '45':
            fan_domain.call_service('turn_off', 'fan.cooling_fan')  # turn off fan in the cabinet
        sleep(10)  # sleep to avoid making too many requests


if __name__ == '__main__':
    main()
