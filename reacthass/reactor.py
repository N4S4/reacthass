from homeassistant_api import Client
from requests_cache import CachedSession
from homeassistant_api import State

import logging
from datetime import timedelta

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.ERROR)


class Reactor(Client):
    def __init__(self, url: str, token: str,
                 cache_refresh_seconds: int = 30, verify_ssl: bool = True):
        """cache_update_seconds the lower, the more requests are made (high traffic))"""

        self._cache_refresh_seconds = CachedSession(backend="filesystem",
                                                    expire_after=timedelta(seconds=cache_refresh_seconds))

        self._verify_ssl = verify_ssl
        self._url = url
        if not self._url.endswith('/api'):
            self._url = url + '/api'

        super().__init__(self._url, token, cache_session=self._cache_refresh_seconds, verify_ssl=self._verify_ssl,
                         use_async=False)

        self._entity_group = self.get_entities()
        self._url = url
        self._token = token

    def send_value_to_entity(self, entity: str, value: any, attributes: dict = None):
        if attributes:
            return self.set_state(State(state=value, entity_id=entity, attributes=attributes))
        else:
            return self.set_state(State(state=value, entity_id=entity))

    def get_groups(self):
        # with self._client:
        # entity_groups = self._client.get_entities()
        groups = []
        for group in self._entity_group:
            groups.append(group)
        return groups

    def get_entities_name(self, group: str):
        entity_name = []
        for entity in self._entity_group[group].entities:
            entity_name.append(entity)
        return entity_name

    def get_entity_state(self, entity: str):
        state = self.get_entity(entity_id=entity).state.state
        return state

    def get_services(self, domain: str):
        service = self.get_domain(domain)
        return service

    def check_specific_state_in_group(self, group: str, state: any) -> dict:  # check what entity has specific state
        all_states = self.get_states()
        group_states = {}
        for entity in all_states:
            if str(entity.entity_id).startswith(group):
                if entity.state == state:
                    group_states[entity.entity_id] = entity.state
        return group_states

    def if_state_equal_to_value(self, entity: str, threshold_value: any, value_type: str = 'string',
                                operator_type: str = '=='):  # operator_type accept <= >= == != < > operator

        state = self.get_entity_state(entity)
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

    def when_value_reached(self, entity: str, threshold_value: any, value_type: str = 'string',
                           operator_type: str = '=='):  # operator_type accept <= >= == != < > operator

        client = Reactor(self._url, self.token, verify_ssl=self._verify_ssl)
        #initiate a client just for the loop, it is actually used the main Reactor initiatior

        with client:
            while True:
                if self.if_state_equal_to_value(entity, threshold_value, value_type, operator_type):
                    return True
