import os
import logging
import collections
from Config import Configurations, Insights, Persistence
import boto3
from botocore.exceptions import EndpointConnectionError, ParamValidationError, ClientError


def enable_security_hub():

    try:
        aws_connection().enable_security_hub()
    except aws_connection().exceptions.ResourceConflictException as exception:
        logging.info(exception)


def enable_import_findings_for_product():

    try:
        aws_connection().enable_import_findings_for_product(ProductArn=Configurations.get_arn())
    except aws_connection().exceptions.ResourceConflictException as exception:
        logging.info(exception)


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

    client = boto3.client('securityhub',
                          aws_access_key_id=keys.get_configurations()['aws_access_key_id'],
                          aws_secret_access_key=keys.get_configurations()['aws_secret_access_key'],
                          region_name=keys.get_configurations()['region_name']
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


def amazon_security_hub(asff_findings):
    try:

        numbers_deque = collections.deque(asff_findings)
        while bool(numbers_deque):
            if len(numbers_deque) > 100:
                send_list = [numbers_deque.popleft() for _i in range(99)]

                try:
                    aws_connection().batch_import_findings(Findings=send_list)
                except ParamValidationError as pv:

                    logging.error(pv.args[0])
            else:
                send_list = ([numbers_deque.popleft() for _i in range(len(numbers_deque))])

                try:
                    aws_connection().batch_import_findings(Findings=send_list)
                except ParamValidationError as pv:

                    logging.error(pv.args[0])

    except (EndpointConnectionError, ClientError) as exception:

        logging.error(exception)


def amazon_security_hub_xml(asff_findings, xml_file_name):
    try:
        try:

            response = aws_connection().batch_import_findings(Findings=asff_findings)

        except ParamValidationError as pv:
            logging.error(pv.args[0])

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            os.remove(xml_file_name)

    except (EndpointConnectionError, ClientError) as exception:

        logging.error(exception)


def insight_creator():
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

    except (EndpointConnectionError, ClientError) as exception:

        logging.error(exception)
