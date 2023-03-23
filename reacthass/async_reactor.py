from homeassistant_api import Client
from aiohttp_client_cache import CachedSession, FileBackend

import logging
from datetime import timedelta

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.ERROR)


class AsyncReactor(Client):
    def __init__(self, url, token, cache_refresh_seconds, verify_ssl=False):

        self._verify_ssl = verify_ssl
        self._token = token
        self._url = url

        if not self._url.endswith('/api'):
            self._url = url + '/api'

        self._cache_refresh_seconds = CachedSession(cache=FileBackend(expire_after=timedelta(seconds=cache_refresh_seconds)))
        # expire_after= goes in FileBackend() and not outside as the documentation say

        super().__init__(self._url, self._token, async_cache_session=self._cache_refresh_seconds,
                         verify_ssl=self._verify_ssl, use_async=True)

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
