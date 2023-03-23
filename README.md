# ReactHass

## Introduction

First of all I love Python, Home Assistant and Docker, but I also
needed a way to communicate from different devices to Home Assistant 
and do some twisted automations.

You might need this repo for one of this reasons
- Interface Home Assistant with other devices
- There might be the case where you want to run an automation outside Home Assistant
- In some of my cases, was easier to build an automation from Python
- You love Python and Docker

## Install

`pip install reacthass`

## Usage
```python
from reacthass import Reactor

token = 'YOUR TOKEN'
url = 'HOME ASSISTANT URL'


hass = Reactor(url, token)

if hass.when_value_reached('sensor', 'temperature', 30):
    hass.call_service('turn_on', 'fan.fan')
    
```

## Persistence
If you want to keep the sensor record in the database you might add to your configuration.yaml:

```yaml
recorder:
  include:
    entities:
      - sensor.test
```

or if you have another suggestion to keep records of the state made by API let me know opening an issue.

## Examples

Some examples are in the `/examples` folder, <br>


## Credits

This package is built on top of the beautiful [HomeAssistantAPI](https://github.com/GrandMoff100/HomeAssistantAPI)


