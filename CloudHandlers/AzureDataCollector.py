#!/usr/bin/env python3
import requests
from datacollectorapi import client
import logging
import collections
from Config import Configurations


def azure_data_collector(json_records):
    customer_id = Configurations.get_configurations()['AzureCustomerId']
    shared_key = Configurations.get_configurations()['AzureSharedKey']
    log_type = Configurations.get_configurations()['LogName']

    api = client.DataCollectorAPIClient(customer_id, shared_key)

    numbers_deque = collections.deque(json_records)
    while bool(numbers_deque):
        if len(numbers_deque) > 50:
            send_list = [numbers_deque.popleft() for _i in range(49)]
            try:
                api.post_data(log_type, send_list)
            except requests.exceptions.ConnectionError:
                logging.error('Connection to Azure can not be established')

        else:
            send_list = ([numbers_deque.popleft() for _i in range(len(numbers_deque))])
            try:
                 api.post_data(log_type, send_list)
            except requests.exceptions.ConnectionError:
                logging.error('Connection to Azure can not be established')



