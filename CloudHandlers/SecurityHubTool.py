import json
import os
import collections
import botocore
from botocore.config import Config
from Config import Configurations, Insights, Persistence
import boto3
from botocore.exceptions import EndpointConnectionError, ParamValidationError, ClientError
from loguru import logger

def enable_security_hub():

    try:
        aws_connection().enable_security_hub()
    except (aws_connection().exceptions.ResourceConflictException, botocore.exceptions.ReadTimeoutError) as exception:
        if type(exception) == botocore.exceptions.ReadTimeoutError:
            logger.error(exception)
        elif type(exception) == aws_connection().exceptions.ResourceConflictException:
            logger.info('Account is already subscribed to Security Hub')


def enable_import_findings_for_product():

    test = Configurations.get_arn()
    try:
        aws_connection().enable_import_findings_for_product(ProductArn=test)
    except (aws_connection().exceptions.ResourceConflictException, botocore.exceptions.ReadTimeoutError) as exception:
        if type(exception) == botocore.exceptions.ReadTimeoutError:
            logger.error(exception)
        elif type(exception) == aws_connection().exceptions.ResourceConflictException:
            logger.info('Account Already has enabled import findings for this product')


class CreateInsight:
    keys = Insights()
    try:
        insights = keys.get_keys()['Insights']
    except TypeError:
        insights = '''{
  "Insights": {
    "": {
      "Title": [
        {
          "Comparison": "",
          "Value": ""
        }
      ],
      "RecordState": [
        {
          "Comparison": "",
          "Value": ""
        }
      ],
      "GroupByAttribute": ""
    },
    "": {
      "Title": [
        {
          "Comparison": "",
          "Value": ""
        }
      ],
      "RecordState": [
        {
          "Comparison": "",
          "Value": ""
        }
      ],
      "GroupByAttribute": ""
    }
  }
}'''
    insights_to_create = [*insights]

    def first(self):
        group_attribute = self.insights[self.insights_to_create[0]]['GroupByAttribute']
        del self.insights[self.insights_to_create[0]]['GroupByAttribute']
        filters = self.insights[self.insights_to_create[0]]

        response = aws_connection().create_insight(Name=self.insights_to_create[0],
                                                   Filters=filters,
                                                   GroupByAttribute=group_attribute)
        Persistence.set_arn(response['InsightArn'], 'Top DLP policies being breached')

    def second(self):
        group_attribute = self.insights[self.insights_to_create[1]]['GroupByAttribute']
        del self.insights[self.insights_to_create[1]]['GroupByAttribute']
        filters = self.insights[self.insights_to_create[1]]

        response = aws_connection().create_insight(Name=self.insights_to_create[1],
                                                   Filters=filters,
                                                   GroupByAttribute=group_attribute)
        Persistence.set_arn(response['InsightArn'], 'Forcepoint DLP Incidents by severity')


def aws_connection():
    keys = Configurations()

    config = Config(
        retries={
            'max_attempts': 5,
            'mode': 'standard'
        }
    )
    client = boto3.client('securityhub',
                          aws_access_key_id=keys.get_configurations()['aws_access_key_id'],
                          aws_secret_access_key=keys.get_configurations()['aws_secret_access_key'],
                          region_name=keys.get_configurations()['region_name'],
                          config=config
                          )
    return client


class InsightCreator:

    def indirect(self, i):
        method_name = 'number_' + str(i)
        method = getattr(self, method_name, lambda: 'Invalid')
        return method()

    @staticmethod
    def number_0():
        CreateInsight.first(CreateInsight())

    @staticmethod
    def number_1():
        CreateInsight.second(CreateInsight())


def amazon_security_hub(asff_findings, offset_time, logger_obj):
    try:

        numbers_deque = collections.deque(asff_findings)
        while bool(numbers_deque):
            if len(numbers_deque) > 100:
                send_list = [numbers_deque.popleft() for _i in range(99)]

                try:
                    response = aws_connection().batch_import_findings(Findings=send_list)
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        Persistence().set_date(offset_time, 'AWSUpdateDate')
                        failed_count = response['FailedCount']
                        success_count = response['SuccessCount']
                        logger_obj.info(
                            f' Security Hub successful response, FailedCount : {failed_count}, SuccessCount : {success_count}')
                        if failed_count:
                            FailedFindings = json.dumps(response['FailedFindings'])
                            logger_obj.error(f'Failed Findings - {FailedFindings}')
                except ParamValidationError as e:

                    logger_obj.error(e.args[0])
            else:
                send_list = ([numbers_deque.popleft() for _i in range(len(numbers_deque))])

                try:
                    response = aws_connection().batch_import_findings(Findings=send_list)
                    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        Persistence().set_date(offset_time, 'AWSUpdateDate')
                        failed_count = response['FailedCount']
                        success_count = response['SuccessCount']
                        logger_obj.info(f' Security Hub successful response, FailedCount : {failed_count}, SuccessCount : {success_count}')
                        if failed_count:
                            FailedFindings = json.dumps(response['FailedFindings'])
                            logger_obj.error(f'Failed Findings - {FailedFindings}')
                except ParamValidationError as e:

                    logger_obj.error(e.args[0])

    except (EndpointConnectionError, ClientError) as exception:

        logger_obj.error(exception)


def amazon_security_hub_xml(asff_findings, xml_file_name, logger_obj):
    try:
        try:

            response = aws_connection().batch_import_findings(Findings=asff_findings)

        except ParamValidationError as pv:
            logger_obj.error(pv.args[0])

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            os.remove(xml_file_name)

    except (EndpointConnectionError, ClientError) as exception:

        logger_obj.error(exception)


def insight_creator(logger_obj):
    try:

        get_insights = aws_connection().get_insights()
        if not (get_insights['Insights']):

            CreateInsight.first(CreateInsight())
            CreateInsight.second(CreateInsight())

        else:
            insights_already_created = []

            for insights in get_insights['Insights']:
                insights_already_created.append(insights['InsightArn'])
            i = 0
            for arn in Persistence.get_arn()['ARN'].values():
                if arn not in insights_already_created:
                    if i == 0:
                        CreateInsight.first(CreateInsight())
                    if i == 1:
                        CreateInsight.second(CreateInsight())
                i += 1

    except (EndpointConnectionError, ClientError, botocore.exceptions.ReadTimeoutError) as exception:

        logger_obj.error(exception)
