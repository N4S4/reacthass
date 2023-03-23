from homeassistant_api import Client
from aiohttp_client_cache import CachedSession, FileBackend

import logging
import asyncio
from datetime import timedelta

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.ERROR)


# TODO all working now, clean up all modules

class AsyncReactor(Client):
    def __init__(self, url, token, cache_refresh_seconds, verify_ssl=False):

        self._verify_ssl = verify_ssl
        self._token = token
        self._url = url
        #self._global_request_kwargs = global_request_kwargs
        #self._entity_groups = self.endpoint(self._entity_group_set())

        if not self._url.endswith('/api'):
            self._url = url + '/api'

        self._cache_refresh_seconds = CachedSession(cache=FileBackend(expire_after=timedelta(seconds=cache_refresh_seconds)))
        # expire_after= goes in FileBackend() and not outside as the documentation say

        super().__init__(self._url, self._token, async_cache_session=self._cache_refresh_seconds,
                         verify_ssl=self._verify_ssl, use_async=True)#, global_request_kwargs=self._global_request_kwargs)

    async def _entity_group_set(self):
        groups = await self.get_groups()
        return groups

    async def get_groups(self):
        groups = []
        for group in await self.async_get_entities():
            groups.append(group.group_id)
        return groups

    async def send_value_to_entity(self, entity: str, value: any, attributes: dict = None):
        entity_data = await self.async_get_entity(entity_id=entity)
        if attributes:
            entity_data.state.state = value
            entity_data.state.attributes.update(attributes)
        else:
            entity_data.state.state = value
        await self.async_set_state(entity_data.state)

    async def get_entities_name(self, group: str):
        entity_name = []
        entities = await self.async_get_entities()
        for entity in entities:
            if entity.group_id == group:
                entity_name.append(entity.entities)
        return entity_name

    async def get_entity_state(self, entity_id):
        state = await self.async_get_state(entity_id=entity_id)
        return state.state

    async def get_services(self, domain: str):
        service = await self.async_get_domain(domain)
        return service

    async def check_specific_state_in_group(self, group: str,
                                            state: any) -> dict:  # check what entity has specific state
        all_states = await self.async_get_states()
        group_states = {}
        for entity in all_states:
            if str(entity.entity_id).startswith(group):
                if entity.state == state:
                    group_states[entity.entity_id] = entity.state
        return group_states

    async def if_state_equal_to_value(self, entity: str, threshold_value: any, value_type: str = 'string',
                                      operator_type: str = '=='):  # operator_type accept <= >= == != < > operator

        state = await self.get_entity_state(entity)
        if type(threshold_value) != type(state):
            return f'Cannot compare threshold type {type(threshold_value)} with state {type(state)}'

        if value_type == 'string':
            if state == threshold_value:
                return True
            else:
                return False

        elif value_type == 'number':
            if operator_type == '==':
                if state == threshold_value:
                    return True
            elif operator_type == '>=':
                if state >= threshold_value:
                    return True
            elif operator_type == '<=':
                if state <= threshold_value:
                    return True
            elif operator_type == '<':
                if state < threshold_value:
                    return True
            elif operator_type == '>':
                if state > threshold_value:
                    return True
            elif operator_type == '!=':
                if state != threshold_value:
                    return True
        else:
            return False

    async def when_value_reached(self, client, entity: str, threshold_value: any, value_type: str = 'string',
                                 operator_type: str = '=='):  # operator_type accept <= >= == != < > operator
        async with client:
            while True:
                if await self.if_state_equal_to_value(entity, threshold_value, value_type, operator_type):
                    return True


if __name__ == '__main__':
    hassurl = 'https://renasa.hopto.me'  # 'https://192.168.1.23:8123'
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjYTgxZDFkOWRhNWE0YjAzOWI1MmUxNmYxZDU0YTVkNiIsImlhdCI6MTY3Nzk2NjI4NywiZXhwIjoxOTkzMzI2Mjg3fQ._xpkNIiIR7ugYm61mbwbYwR8S1QJ2vtIg4ceh9R23JI'

    react = AsyncReactor(hassurl, token, cache_refresh_seconds=10, verify_ssl=False)


    async def test1():
        door = await react.async_get_state(entity_id='sensor.temperature_11')
        return door


    async def test2():
        door = await react.get_groups()
        return door


    async def test3():
        door = await react.send_value_to_entity('sensor.testing', 'on', attributes={'light': 'on', 'temperature': '23'})
        return door


    async def test4():
        door = await react.get_entities_name('person')
        return door


    async def test5():
        door = await react.check_specific_state_in_group('person', 'not_home')
        return door


    async def test6():
        door = await react.if_state_equal_to_value('sensor.testing', 'off')
        return door


    async def test7():
        async with react:
            while True:
                door = await react.get_entity_state('sensor.testing')
                if door == 'on':
                    return True
                else:
                    print(door)
                # await asyncio.sleep(1)

    async def test8():
        door = await react.when_value_reached(react, 'sensor.testing', 'on')
        return door

    async def test9():  # update entity every 10 seconds
        while True:
            dummy = await react.get_entity_state('sensor.testing')

            if dummy == 'on':
                await react.send_value_to_entity('sensor.testing', 'off')
            else:
                await react.send_value_to_entity('sensor.testing', 'on')

            await asyncio.sleep(10)


    # asyncio.run(test1())
    # print(asyncio.get_event_loop().run_until_complete(test1()))
    # print(asyncio.get_event_loop().run_until_complete(test2()))
    # print(asyncio.get_event_loop().run_until_complete(test3()))
    # print(asyncio.get_event_loop().run_until_complete(test4()))
    # print(asyncio.get_event_loop().run_until_complete(test5()))
    # print(asyncio.get_event_loop().run_until_complete(test6()))
    # print(asyncio.get_event_loop().run_until_complete(test7()))
    #print(asyncio.get_event_loop().run_until_complete(test8()))
    print(asyncio.get_event_loop().run_until_complete(test9()))
