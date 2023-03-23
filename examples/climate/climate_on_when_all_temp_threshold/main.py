from reacthass import Reactor
from time import sleep

# reacthass settings
token = 'YOUR TOKEN'
hassurl = 'HOME ASSISTANT URL'

# Initiate reacthass session
hass = Reactor(hassurl, token, verify_ssl=False)


def main():
    while True:
        climates = hass.get_entities_name('climate')  # get a list of all thermostat
        room1 = hass.get_entity_state('sensor.temperature_1')  # temperature sensors state
        room2 = hass.get_entity_state('sensor.temperature_2')
        room3 = hass.get_entity_state('sensor.temperature_3')

        if room1 and room2 and room3 <= '18':  # check if all 3 rooms are below 18C
            for climate in climates:  # loop through all climates names
                entity = hass.get_domain('climate')  # get doamin to call service
                return entity.turn_on(entity_id='climate.' + climate)  # for every climate call service


if __name__ == '__main__':
    main()
