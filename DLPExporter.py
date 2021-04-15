# !/usr/bin/env python3
import os
import time
import pyodbc
import ASFFMapper as Mapper
import DatabaseConnector
from logger import LogConfig
from CloudHandlers.AzureDataCollector import azure_data_collector
from CloudHandlers.SecurityHubTool import amazon_security_hub, insight_creator, amazon_security_hub_xml, \
    enable_security_hub, enable_import_findings_for_product
from Config import Configurations, DatabaseConnection
from xmltodict import parse
from threading import Thread
import logging
import argparse


class ManualAWS(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            location = Configurations.get_configurations()['file_location']

            for file in os.listdir(location):
                if file.endswith(".xml") and file.startswith("event"):
                    with open(os.path.join(location, file)) as fd:
                        doc = parse(fd.read())

                        xml_file_name = location + '/event-' + doc['evt:event']['evt:event_info'][
                            'evt:incidentId'] + '.xml'

                        json_file = Mapper.map_xml_to_asff(doc)

                        fd.close()

                        # Dont send empty files
                        if (len(json_file)) >= 1:
                            amazon_security_hub_xml(json_file, xml_file_name)
                        else:
                            os.remove(xml_file_name)
            time.sleep(10)


class AzureAutoCheck(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:

            json_file = Mapper.map_sql_to_azure()
            if not json_file:
                time.sleep(300)
            elif (len(json_file)) >= 1:
                azure_data_collector(json_file)


class AWSAutoCheck(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):

        while True:

            json_file = Mapper.map_sql_to_asff()
            if not json_file:
                time.sleep(300)
            elif (len(json_file)) >= 1:
                amazon_security_hub(json_file)


class CreateInsight(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        insight_creator()


if __name__ == "__main__":
    LogConfig()

    parser = argparse.ArgumentParser(description='DLPExporter')
    parser.add_argument('--key', action="store", dest='key', default='0')
    parser.add_argument('--password', action="store", dest='password', default='0')
    parser.add_argument('--username', action="store", dest='username', default='0')
    args = parser.parse_args()
    config = Configurations.get_configurations()
    if config['Database_Connection']['Trusted_Connection'] == 'no' and (args.key == 0 or '0'):
        key = DatabaseConnection.save_password(args.password, args.username)
        f = open("secret-key.txt", "w")
        f.write(key)
        f.close()
    elif config['Database_Connection']['Trusted_Connection'] == 'no' and (args.key == 0 or '0'):
        config.set_key(args.key)
    try:
        if config['AwsAccountId'] and config['aws_access_key_id'] \
                and config['aws_secret_access_key'] and config['region_name']:
            logging.info('AWS is configured on')
            try:
                if DatabaseConnection.get_connection() != 'none':
                    enable_security_hub()
                    enable_import_findings_for_product()
                    DatabaseConnector.execute_sql('SELECT @@version')
                    logging.info('Database Connection established - AWS thread starting')
                    CreateInsight()
                    ManualAWS()
                    AWSAutoCheck()

            except pyodbc.Error as ex:
                logging.error(ex.args[1])
        else:
            logging.info("configure the config.json if you need AWS")
    except KeyError:
        logging.info("Ignore if not using Security Hub. Some fields are missing from the config (AwsAccountId, "
                     "aws_access_key_id, aws_secret_access_key, region_name)")

    try:
        if config['AzureCustomerId'] and config['AzureSharedKey']:
            logging.info('Azure is configured on')

            try:
                if DatabaseConnection.get_connection() != 'none':
                    DatabaseConnector.execute_sql('SELECT @@version')
                    logging.info('Database Connection established - Azure thread starting')

                    AzureAutoCheck()
            except pyodbc.Error as ex:
                logging.error(ex.args[1])
        else:
            logging.info("configure the config.json if you need azure")
    except KeyError:
        logging.info("Ignore if not using Sentinel. Some fields are missing from the config (AzureCustomerId, "
                     "AzureSharedKey)")

    os.system("pause")
