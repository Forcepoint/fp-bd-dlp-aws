#!/usr/bin/env python3
from datacollectorapiMOD import client
import logging
import collections
from Config import Configurations, Persistence


def azure_api_call(customer_id, shared_key, log_type, send_list, offset_time):
    api = client.DataCollectorAPIClient(customer_id, shared_key)
    result = api.post_data(log_type, send_list, timeout=30.0)
    if result.status_code != 200:
        logging.info(f'Error azure api response: {result.status_code}')
    else:
        logging.info(f'Successful azure api response: {result.status_code}')
        if offset_time is not None:
            Persistence().set_date(str(offset_time), 'AzureUpdateDate')


def azure_data_collector(json_records, offset_time):
    customer_id = Configurations.get_configurations()['AzureWorkspaceID']
    shared_key = Configurations.get_configurations()['AzurePrimaryKey']
    log_type = Configurations.get_configurations()['LogName']

    numbers_deque = collections.deque(json_records)

    while bool(numbers_deque):

        if len(numbers_deque) > 50:
            send_list = [numbers_deque.popleft() for _i in range(49)]
            azure_api_call(customer_id, shared_key, log_type, send_list, offset_time)

        else:
            send_list = ([numbers_deque.popleft() for _i in range(len(numbers_deque))])
            azure_api_call(customer_id, shared_key, log_type, send_list, offset_time)
