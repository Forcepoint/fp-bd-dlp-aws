import json
import datetime

from JsonFormatClass import JsonFormatClass, Network, Finding, RelatedFinding, Resource, Details, ProductFields, \
    Severity, UserDefinedFields
from Config import Configurations, Persistence
from DatabaseConnector import get_events, execute_policy_events, \
    query_events, query_services, query_users, query_domains, query_destinations_users, query_policy_categories
from ExtraFields import ExtraData


def remove_null_items(d):
    if type(d) is dict:
        return dict((k, remove_null_items(v)) for k, v in d.items() if v and remove_null_items(v))
    elif type(d) is list:
        return [remove_null_items(v) for v in d if v and remove_null_items(v)]
    else:
        return d


def __iso8601_format(time):
    date_time_obj = datetime.time()
    try:
        date_time_obj = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        pass

    try:
        date_time_obj = datetime.datetime.strptime(time, '%d-%m-%Y %H:%M:%S')
    except ValueError:
        pass

    try:
        date_time_obj = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    except ValueError:
        pass

    return date_time_obj.strftime('%Y-%m-%dT%H:%M:%SZ').__str__()


def __normalized_severity(severity_dlp):
    switcher = {
        'LOW': 20,
        'MEDIUM': 50,
        'HIGH': 95
    }
    return switcher.get(severity_dlp, 0)


def __normalized_severity_from_db(severity_dlp):
    switcher = {
        3: 'LOW',
        2: 'MEDIUM',
        1: 'HIGH'
    }
    return switcher.get(severity_dlp, 0)


def __severity_label(severity_dlp):
    switcher = {
        3: 'LOW',
        2: 'MEDIUM',
        1: 'CRITICAL'
    }
    return switcher.get(severity_dlp, 0)


def __normalized_network_direction(network_direction):
    switcher = {
        'TO': 'OUT',
        'FROM': 'IN',
    }
    return switcher.get(network_direction, 0)


def destinations_mapping(event, extra_data):
    destinations_array_length = int(event['evt:event']['evt:event_info']['evt:destinations']['evt:Count'])

    network_destinations_object = {}
    if destinations_array_length > 1:
        for i in range(destinations_array_length):
            if i == 0 and destinations_array_length > 1:
                network_destinations_object['DestinationDomain'] = \
                    event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i]['evt:event_user'][
                        'evt:domain']
                network_destinations_object['DestinationIpV4'] = \
                    event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i]['evt:event_user'][
                        'evt:ip']
                network_destinations_object['DestinationPort'] = \
                    event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i]['evt:event_user'][
                        'evt:port']
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:commonName']], 'DestinationCommonName')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:username']], 'DestinationUsername')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:hostname']], 'DestinationHostname')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:email']], 'DestinationEmail')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:extra_data']], 'DestinationExtraData')

            elif i > 0 and destinations_array_length > 1:
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:domain']], 'DestinationDomain')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:ip']], 'DestinationIpV4')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:port']], 'DestinationPort')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:commonName']], 'DestinationCommonName')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:username']], 'DestinationUsername')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:hostname']], 'DestinationHostname')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:email']], 'DestinationEmail')
                extra_data.extra_data_handler(
                    [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][i][
                         'evt:event_user']['evt:extra_data']], 'DestinationExtraData')

    else:
        network_destinations_object['DestinationDomain'] = \
            event['evt:event']['evt:event_info']['evt:destinations']['evt:destination']['evt:event_user'][
                'evt:domain']
        network_destinations_object['DestinationIpV4'] = \
            event['evt:event']['evt:event_info']['evt:destinations']['evt:destination']['evt:event_user'][
                'evt:ip']
        network_destinations_object['DestinationPort'] = \
            (event['evt:event']['evt:event_info']['evt:destinations']['evt:destination']['evt:event_user'][
                'evt:port'])
        extra_data.extra_data_handler([event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][
                                           'evt:event_user']['evt:commonName']], 'DestinationCommonName')
        extra_data.extra_data_handler([event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][
                                           'evt:event_user']['evt:username']], 'DestinationUsername')
        extra_data.extra_data_handler([event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][
                                           'evt:event_user']['evt:hostname']], 'DestinationHostname')
        extra_data.extra_data_handler([event['evt:event']['evt:event_info']['evt:destinations']['evt:destination'][
                                           'evt:event_user']['evt:email']], 'DestinationEmail')
        extra_data.extra_data_handler(
            [event['evt:event']['evt:event_info']['evt:destinations']['evt:destination']['evt:event_user'][
                 'evt:extra_data']], 'DestinationExtraData')

    return network_destinations_object, extra_data


def map_xml_to_asff(event):
    findings_array_length = int(event['evt:event']['evt:rules']['evt:Count'])
    findings = []
    keys = Configurations()

    for i in range(findings_array_length):
        extra_data = ExtraData()
        findings_object = Finding()
        findings_object.GeneratorId = event['evt:event']['evt:event_info']['evt:incidentId']
        findings_object.AwsAccountId = keys.get_configurations()['AwsAccountId'][:12]
        findings_object.CreatedAt = __iso8601_format(event['evt:event']['evt:event_info']['evt:insert_date'])
        findings_object.Description = event['evt:event']['evt:event_info']['evt:subject'] or "Description Not found"

        network_object = Network()
        network_object.Protocol = event['evt:event']['evt:event_info']['evt:channel']['evt:protocol'].split("_")[1]
        network_object.SourceDomain = event['evt:event']['evt:event_info']['evt:source']['evt:event_user']['evt:domain']
        network_object.SourceIpV4 = event['evt:event']['evt:event_info']['evt:source']['evt:event_user']['evt:ip']
        network_object.SourcePort = event['evt:event']['evt:event_info']['evt:source']['evt:event_user']['evt:port']

        findings_object.ProductArn = keys.get_arn()

        related_findings_object = RelatedFinding()
        related_findings_object.Id = event['evt:event']['evt:event_info']['evt:eventId'][:512]
        related_findings_object.ProductArn = keys.get_arn()

        findings_object.RelatedFindings = [related_findings_object.__dict__]
        findings_object.SchemaVersion = '2018-10-08'
        findings_object.Title = 'Forcepoint DLP Incident'
        findings_object.Types = ['Sensitive Data Identifications/Security/ForcepointDLP']
        findings_object.UpdatedAt = __iso8601_format(event['evt:event']['evt:event_info']['evt:insert_date'])

        resource_object = Resource()

        details_object = Details()
        product_fields_object = ProductFields()
        product_fields_object.ForcepointDLPSourceIP = \
            event['evt:event']['evt:event_info']['evt:source']['evt:event_user']['evt:ip']
        product_fields_object.Text = event['evt:event']['evt:event_info']['evt:channel']['evt:service_name']
        product_fields_object.UpdatedAt = __iso8601_format(event['evt:event']['evt:event_info']['evt:insert_date'])
        product_fields_object.UpdatedBy = event['evt:event']['evt:event_info']['evt:channel']['evt:agent_name']

        extra_data.extra_data_handler([event['evt:event']['evt:event_info']['evt:source']['evt:event_user'][
                                           'evt:email']], 'SourceEmail')
        extra_data.extra_data_handler([event['evt:event']['evt:event_info']['evt:source']['evt:event_user'][
                                           'evt:extra_data']], 'SourceExtraData')
        extra_data.extra_data_handler([event['evt:event']['evt:event_info']['evt:source']['evt:event_user'][
                                           'evt:full_name']], 'SourceFullName')
        extra_data.extra_data_handler([event['evt:event']['evt:event_info']['evt:source']['evt:event_user'][
                                           'evt:hostname']], 'SourceHostname')
        extra_data.extra_data_handler([event['evt:event']['evt:event_info']['evt:source']['evt:event_user'][
                                           'evt:login_name']], 'SourceLoginName')
        extra_data.extra_data_handler([event['evt:event']['evt:event_info']['evt:source']['evt:event_user'][
                                           'evt:username']], 'SourceUsername')

        network_destinations_object, extra_data = destinations_mapping(event, extra_data)

        network_object.__dict__.update(network_destinations_object)
        details_object.Other = product_fields_object.__dict__
        resource_object.Type = 'Other'
        resource_object.Details = details_object.__dict__
        severity_object = Severity()

        if int((event['evt:event']['evt:rules']['evt:Count'])) == 1:

            findings_object.Id = 'incident_Id:' + event['evt:event']['evt:event_info']['evt:incidentId'][
                                                  :512] + '-rule_id:' + \
                                 event['evt:event']['evt:rules']['evt:rule']['evt:rule_id']
            severity_object.Normalized = event['evt:event']['evt:rules']['evt:rule']['evt:severity'] or 'LOW'
            resource_object.Id = event['evt:event']['evt:rules']['evt:rule']['evt:policy_name']
            extra_data.extra_data_handler([event['evt:event']['evt:rules']['evt:rule']['evt:rule_name'][:512]],
                                          'RuleName')

        elif int(event['evt:event']['evt:rules']['evt:Count']) > 1:

            findings_object.Id = 'incident_Id:' + event['evt:event']['evt:event_info']['evt:incidentId'][
                                                  :512] + '-rule_id:' + \
                                 event['evt:event']['evt:rules']['evt:rule'][i]['evt:rule_id']
            severity_object.Normalized = event['evt:event']['evt:rules']['evt:rule'][i]['evt:severity'] or 'LOW'
            resource_object.Id = event['evt:event']['evt:rules']['evt:rule'][i]['evt:policy_name']
            extra_data.extra_data_handler([event['evt:event']['evt:rules']['evt:rule'][i]['evt:rule_name'][:512]],
                                          'Rule_name')

        findings_object.Severity = severity_object.__dict__
        details_object.Other.update(extra_data.extra_data_storage)
        findings_object.Network = network_object.__dict__
        findings_object.Resources = [resource_object.__dict__]
        findings.append(findings_object.__dict__)

    asff_object = JsonFormatClass()

    asff_object.findings = findings

    cleaned_findings = remove_null_items(asff_object.findings)

    for finding in cleaned_findings:
        i = 0
        if finding['Severity']['Normalized']:
            if not (keys.get_configurations()[finding['Severity']['Normalized']]):
                del cleaned_findings[i]
        i += 1

    for i in range(len(cleaned_findings)):
        cleaned_findings[i]['Severity']['Normalized'] = (
            __normalized_severity(cleaned_findings[i]['Severity']['Normalized']))

    return cleaned_findings


def map_sql_to_azure():
    event_list, partitions = get_events('AzureUpdateDate')

    if bool(partitions):

        event_list, partitions = get_events('AzureUpdateDate')
        logs = []

        for partition in partitions:

            for row in event_list:

                policy_events = execute_policy_events(partition, row[0])

                for policy in policy_events:
                    extra_data_sql = ExtraData()
                    event_data = query_events(partition, row[0])
                    service_id = event_data[0].SERVICE_ID
                    source_id = event_data[0].SOURCE_ID

                    user_data = query_users(source_id)
                    domain_id = user_data[0].DOMAIN_ID

                    services_data = query_services(service_id)
                    destination_data = query_destinations_users(partition, row[0])
                    formatted_date = __iso8601_format(
                        json.dumps(event_data[0].INSERT_DATE, indent=4, sort_keys=True,
                                   default=str)[1:-4])

                    findings_object = Finding()
                    findings_object.GeneratorId = str(event_data[0].ID)
                    findings_object.CreatedAt = formatted_date
                    findings_object.Description = event_data[0].SUBJECT or "Description Not found"

                    findings_object.Protocol = services_data[0].PROTOCOL_ID.split("_")[1]
                    if domain_id is not None:
                        findings_object.SourceDomain = query_domains(domain_id)[0].NAME
                    else:
                        findings_object.SourceDomain = 'none'
                    findings_object.SourceIpV4 = user_data[0].IP
                    findings_object.SourcePort = event_data[0].PORT

                    if destination_data[0][0].DOMAIN_ID is not None:
                        findings_object.DestinationDomain = query_domains(destination_data[0][0].DOMAIN_ID)[0].NAME
                    else:
                        findings_object.DestinationDomain = 'none'

                    findings_object.DestinationIpV4 = destination_data[0][0].IP
                    findings_object.DestinationPort = destination_data[0][0].PORT

                    findings_object.ExternalId = event_data[0].EXTERNAL_ID

                    findings_object.Title = 'Forcepoint DLP Incident'
                    findings_object.UpdatedAt = formatted_date

                    findings_object.ForcepointDLPSourceIP = user_data[0].IP
                    findings_object.Text = services_data[0].CHANNEL_NAME
                    findings_object.UpdatedAt = formatted_date
                    findings_object.UpdatedBy = services_data[0].AGENT_NAME

                    extra_data_sql.extra_data_handler([query_policy_categories(policy.POLICY_CATEGORY_ID)[0].NAME],
                                                      'RuleName')
                    extra_data_sql.extra_data_handler([user_data[0].EMAIL], 'SourceEmail')
                    extra_data_sql.extra_data_handler([user_data[0].EXTRA_DATA], 'SourceExtraData')
                    extra_data_sql.extra_data_handler([user_data[0].FULL_NAME], 'SourceFullName')
                    extra_data_sql.extra_data_handler([user_data[0].HOSTNAME], 'SourceHostname')
                    extra_data_sql.extra_data_handler([user_data[0].LOGIN_NAME], 'SourceLoginName')
                    # extra_data_sql.extra_data_handler([user_data[0].Username], 'SourceUsername')

                    for i in range(len(destination_data)):
                        extra_data_sql.extra_data_handler([destination_data[i][0].COMMON_NAME], 'DestinationCommonName')
                        # user_defined_extras['DestinationUsername.' + str(i + 1)]
                        extra_data_sql.extra_data_handler([destination_data[i][0].HOSTNAME], 'DestinationHostname')
                        extra_data_sql.extra_data_handler([destination_data[i][0].EMAIL], 'DestinationEmail')
                        extra_data_sql.extra_data_handler([destination_data[i][0].EXTRA_DATA], 'DestinationExtraData')
                        if i >= 1:
                            if destination_data[i][0].DOMAIN_ID is not None:
                                extra_data_sql.extra_data_handler([query_domains(destination_data[i][0].DOMAIN_ID)[
                                                                       0].NAME], 'DestinationDomain')

                            else:
                                findings_object.DestinationDomain = 'none'
                            extra_data_sql.extra_data_handler([destination_data[i][0].IP], 'DestinationIpV4')
                            extra_data_sql.extra_data_handler([destination_data[i][0].PORT], 'DestinationPort')

                    findings_object.Type = 'Forcepoint DLP'

                    findings_object.Id = 'incident_Id-%s-rule_id-%s' % (row[0], policy[0])
                    findings_object.Severity = policy.SEVERITY
                    findings_object.PolicyCategoryId = str(query_policy_categories(policy.POLICY_CATEGORY_ID)[0].ID)
                    findings_object.__dict__.update(extra_data_sql.extra_data_storage)
                    logs.append(findings_object.__dict__)

        logs_object = JsonFormatClass()

        logs_object.findings = logs

        cleaned_findings = remove_null_items(logs_object.findings)

        for i in range(len(cleaned_findings)):
            pos = i - 1
            if cleaned_findings[pos]['Severity']:
                if not (
                        Configurations.get_configurations()[
                            __normalized_severity_from_db(
                                cleaned_findings[pos]['Severity'])]):
                    del cleaned_findings[pos]

        for i in range(len(cleaned_findings)):
            cleaned_findings[i]['Severity'] = __normalized_severity_from_db(cleaned_findings[i]['Severity'])

        if cleaned_findings.__len__() >= 1:
            date_time_obj = datetime.datetime.strptime(cleaned_findings[-1]["CreatedAt"], '%Y-%m-%dT%H:%M:%SZ')
            offset_time = date_time_obj + datetime.timedelta(seconds=1)
            Persistence().set_date(str(offset_time), 'AzureUpdateDate')

        return cleaned_findings
    else:
        return False


def map_sql_to_asff():
    event_list, partitions = get_events('AWSUpdateDate')

    if bool(partitions):

        event_list, partitions = get_events('AWSUpdateDate')
        findings = []

        for partition in partitions:

            for row in event_list:

                policy_events = execute_policy_events(partition, row[0])

                for policy in policy_events:
                    extra_data_sql = ExtraData()
                    event_data = query_events(partition, row[0])
                    service_id = event_data[0].SERVICE_ID
                    source_id = event_data[0].SOURCE_ID

                    user_data = query_users(source_id)
                    domain_id = user_data[0].DOMAIN_ID

                    services_data = query_services(service_id)
                    destination_data = query_destinations_users(partition, row[0])
                    asff_date = __iso8601_format(
                        json.dumps(event_data[0].INSERT_DATE, indent=4, sort_keys=True,
                                   default=str)[1:-4])

                    findings_object = Finding()
                    findings_object.GeneratorId = str(event_data[0].ID)
                    findings_object.AwsAccountId = Configurations.get_configurations()['AwsAccountId'][:12]
                    findings_object.CreatedAt = asff_date
                    findings_object.Description = event_data[0].SUBJECT or "Description Not found"
                    network_object = Network()

                    network_object.Protocol = services_data[0].PROTOCOL_ID.split("_")[1]
                    if domain_id is not None:
                        network_object.SourceDomain = query_domains(domain_id)[0].NAME
                    else:
                        network_object.SourceDomain = 'none'
                    network_object.SourceIpV4 = user_data[0].IP
                    network_object.SourcePort = event_data[0].PORT

                    if destination_data[0][0].DOMAIN_ID is not None:
                        network_object.DestinationDomain = query_domains(destination_data[0][0].DOMAIN_ID)[0].NAME
                    else:
                        network_object.DestinationDomain = 'none'

                    network_object.DestinationIpV4 = destination_data[0][0].IP
                    network_object.DestinationPort = destination_data[0][0].PORT

                    findings_object.ProductArn = Configurations.get_arn()

                    related_findings_object = RelatedFinding()
                    related_findings_object.Id = event_data[0].EXTERNAL_ID
                    related_findings_object.ProductArn = Configurations.get_arn()

                    findings_object.SchemaVersion = '2018-10-08'
                    findings_object.Title = 'Forcepoint DLP Incident'
                    findings_object.Types = ['Sensitive Data Identifications/Security/ForcepointDLP']
                    findings_object.UpdatedAt = asff_date

                    resource_object = Resource()
                    details_object = Details()

                    product_fields_object = ProductFields()
                    product_fields_object.ForcepointDLPSourceIP = user_data[0].IP
                    product_fields_object.Text = services_data[0].CHANNEL_NAME
                    product_fields_object.UpdatedAt = asff_date
                    product_fields_object.UpdatedBy = services_data[0].AGENT_NAME

                    extra_data_sql.extra_data_handler([query_policy_categories(policy.POLICY_CATEGORY_ID)[0].NAME],
                                                      'RuleName')
                    extra_data_sql.extra_data_handler([user_data[0].EMAIL], 'SourceEmail')
                    extra_data_sql.extra_data_handler([user_data[0].EXTRA_DATA], 'SourceExtraData')
                    extra_data_sql.extra_data_handler([user_data[0].FULL_NAME], 'SourceFullName')
                    extra_data_sql.extra_data_handler([user_data[0].HOSTNAME], 'SourceHostname')
                    extra_data_sql.extra_data_handler([user_data[0].LOGIN_NAME], 'SourceLoginName')
                    # extra_data_sql.extra_data_handler([user_data[0].Username], 'SourceUsername')

                    for i in range(len(destination_data)):
                        extra_data_sql.extra_data_handler([destination_data[i][0].COMMON_NAME], 'DestinationCommonName')
                        # user_defined_extras['DestinationUsername.' + str(i + 1)]
                        extra_data_sql.extra_data_handler([destination_data[i][0].HOSTNAME], 'DestinationHostname')
                        extra_data_sql.extra_data_handler([destination_data[i][0].EMAIL], 'DestinationEmail')
                        extra_data_sql.extra_data_handler([destination_data[i][0].EXTRA_DATA], 'DestinationExtraData')
                        if i >= 1:
                            if destination_data[i][0].DOMAIN_ID is not None:
                                extra_data_sql.extra_data_handler([query_domains(destination_data[i][0].DOMAIN_ID)[
                                                                       0].NAME], 'DestinationDomain')

                            else:
                                network_object.DestinationDomain = 'none'
                            extra_data_sql.extra_data_handler([destination_data[i][0].IP], 'DestinationIpV4')
                            extra_data_sql.extra_data_handler([destination_data[i][0].PORT], 'DestinationPort')

                    resource_object.Type = 'Forcepoint DLP'
                    resource_object.Details = details_object.__dict__
                    severity_object = Severity()

                    findings_object.Id = 'incident_Id-%s-rule_id-%s' % (row[0], policy[0])
                    severity_object.Normalized = policy.SEVERITY
                    severity_object.Product = policy.SEVERITY
                    severity_object.Label = 'none'
                    resource_object.Id = str(query_policy_categories(policy.POLICY_CATEGORY_ID)[0].ID)

                    findings_object.Resources = [resource_object.__dict__]
                    findings_object.Severity = severity_object.__dict__
                    findings_object.Network = network_object.__dict__
                    findings_object.RelatedFindings = [related_findings_object.__dict__]
                    details_object.Other = product_fields_object.__dict__
                    details_other = extra_data_sql.take(50)
                    details_object.Other.update(details_other)
                    extra_data_sql.remove_dups(details_other)
                    product_fields = extra_data_sql.take(50)
                    findings_object.ProductFields = product_fields
                    findings.append(findings_object.__dict__)

        asff_object = JsonFormatClass()

        asff_object.findings = findings

        cleaned_findings = remove_null_items(asff_object.findings)

        for i in range(len(cleaned_findings)):
            pos = i - 1
            if cleaned_findings[pos]['Severity']['Normalized']:
                if not (
                        Configurations.get_configurations()[
                            __normalized_severity_from_db(cleaned_findings[pos]['Severity']['Normalized'])]):
                    del cleaned_findings[pos]

        for i in range(len(cleaned_findings)):
            cleaned_findings[i]['Severity']['Label'] = __severity_label(cleaned_findings[i]['Severity']['Normalized'])
            cleaned_findings[i]['Severity']['Normalized'] = (__normalized_severity(__normalized_severity_from_db(cleaned_findings[i]['Severity']['Normalized'])))

        if cleaned_findings.__len__() >= 1:
            date_time_obj = datetime.datetime.strptime(cleaned_findings[-1]["CreatedAt"], '%Y-%m-%dT%H:%M:%SZ')
            offset_time = date_time_obj + datetime.timedelta(seconds=1)
            Persistence().set_date(str(offset_time), 'AWSUpdateDate')

        return cleaned_findings
    else:
        return False
