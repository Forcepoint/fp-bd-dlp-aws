#!/usr/bin/env python3
import requests
from datacollectorapiMOD import client
import logging
import collections

from requests import ReadTimeout

from Config import Configurations, Persistence


def azure_api_call(customer_id, shared_key, log_type, send_list, offset_time):
    api = client.DataCollectorAPIClient(customer_id, shared_key)
    try:
        health = api.health_check(log_type)
        if health.status_code != 500:
            result = api.post_data(log_type, send_list, timeout=30.0)
            if result.status_code != 200:
                logging.info(f'azure api response: {result.status_code}')
            else:
                logging.info(f'azure api response: {result.status_code}')
                if offset_time is not None:
                    Persistence().set_date(str(offset_time), 'AzureUpdateDate')
        else:
            logging.error(f'Connection to Azure cannot be established, please check your internet connection')
    except (requests.exceptions.ConnectionError, ReadTimeout) as e:
        logging.error(f'{e}: error occurred')


def azure_data_collector(json_records, offset_time):
    customer_id = Configurations.get_configurations()['AzureCustomerId']
    shared_key = Configurations.get_configurations()['AzureSharedKey']
    log_type = Configurations.get_configurations()['LogName']

    numbers_deque = collections.deque(json_records)

    while bool(numbers_deque):

        if len(numbers_deque) > 50:
            send_list = [numbers_deque.popleft() for _i in range(49)]
            azure_api_call(customer_id, shared_key, log_type, send_list, offset_time)

        else:
            send_list = ([numbers_deque.popleft() for _i in range(len(numbers_deque))])
            azure_api_call(customer_id, shared_key, log_type, send_list, offset_time)
