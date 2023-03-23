from reacthass import Reactor
from time import sleep

# reacthass settings
token = 'YOUR TOKEN'
hassurl = 'HOME ASSISTANT URL'

# Initiate reacthass session
hass = Reactor(hassurl, token, verify_ssl=False)


def main():
    while True:
        person = 'person.renato'
        check = hass.if_state_equal_to_value(person, 'not_home')

        if check:  # checks if state is true
            lights_on = hass.check_specific_state_in_group('light', 'on')  # checks what lights are on and return a dict
            for entity_name in lights_on:  # iterate through returned dict
                domain = hass.get_domain('light')
                domain.turn_off(entity_name)  # turn off every entity that is on
                pass
        sleep(60*5)  # check every 5 minutes


if __name__ == '__main':
    main()
