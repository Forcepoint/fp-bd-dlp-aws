#!/usr/bin/env python3
import requests
from datacollectorapiMOD import client
import logging
import collections

from requests import ReadTimeout

from Config import Configurations


def azure_api_call(customer_id, shared_key, log_type, send_list):
    api = client.DataCollectorAPIClient(customer_id, shared_key)
    try:
        result = api.post_data(log_type, send_list, timeout=30.0)
        if result:
            logging.info(f'azure api response: {result}')
    except (requests.exceptions.ConnectionError, ReadTimeout) as e:
        logging.error(f'{e}: error occurred')


def azure_data_collector(json_records):
    customer_id = Configurations.get_configurations()['AzureCustomerId']
    shared_key = Configurations.get_configurations()['AzureSharedKey']
    log_type = Configurations.get_configurations()['LogName']

    numbers_deque = collections.deque(json_records)

    while bool(numbers_deque):

        if len(numbers_deque) > 50:
            send_list = [numbers_deque.popleft() for _i in range(49)]
            azure_api_call(customer_id, shared_key, log_type, send_list)

        else:
            send_list = ([numbers_deque.popleft() for _i in range(len(numbers_deque))])
            azure_api_call(customer_id, shared_key, log_type, send_list)
