from reacthass import Reactor
from time import sleep

# reacthass settings
token = 'YOUR TOKEN'
hassurl = 'HOME ASSISTANT URL'

# Initiate reacthass session
hass = Reactor(hassurl, token, verify_ssl=False)


def main():
    while True:
        power_load = hass.get_entity_state('sensor.power')  # get KW consumed
        # Get all power users
        users = dict(oven='switch.oven',
                     heater_room='switch.heater_room',
                     heater_kids='switch.heater_kids',
                     water_heater='switch.water_heater',
                     fan='switch.fan', )

        what_user_on = {}

        for user in users:  # adds to the list only the users that are on
            if users[user] == 'on':
                what_user_on[user] = users[user]

        if power_load >= '4000':  # Watt or 4 Kw
            for user in what_user_on:
                domain = hass.get_domain(what_user_on[user])  # get the domain of each user in the dict
                domain.turn_off(what_user_on[user])
                if power_load == '3000':  # when reach just a safe number
                    pass
        sleep(1)  # check every second


if __name__ == '__main__':
    main()
