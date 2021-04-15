import pyodbc
from Config import Persistence, DatabaseConnection


class reg(object):
    def __init__(self, cursor, row):
        for (attr, val) in zip((d[0] for d in cursor.description), row):
            setattr(self, attr, val)


def table_fields_by_name(sql):
    rows = []
    cursor = execute_sql(sql)
    for row in list(cursor):
        rows.append(reg(cursor, row))
    return rows


def get_partitions():
    get_partitions = 'SELECT [PARTITION_INDEX] FROM [wbsn-data-security].[dbo].[PA_EVENT_PARTITION_CATALOG]  where ' \
                     'STATUS = \'ONLINE_ACTIVE\' or  STATUS = \'ONLINE\''

    partitions = execute_sql(get_partitions).fetchall()
    normalised_partitions = []
    for partition in partitions:
        normalised_partitions.append(partition[0])

    return normalised_partitions


def get_events(cloud_provider):

    try:
        partitions = get_partitions()

        events_query = 'SELECT TOP (49) * FROM [wbsn-data-security].[dbo].[PA_EVENTS_%s] '
        where_less_than_90 = 'where INSERT_DATE >= dateadd(MM, -3,  getdate()) and [INSERT_DATE] > Convert(datetime, ' \
                             '\'%s\' ) '
        if len(partitions) > 1:
            events_query = events_query % partitions[0]
            events_query += where_less_than_90 % Persistence.get_date(cloud_provider)[cloud_provider]
            for partition in partitions:
                events_query += 'UNION ALL SELECT * FROM [wbsn-data-security].[dbo].[PA_EVENTS_%s]' % partition
                events_query += where_less_than_90 % Persistence.get_date(cloud_provider)[cloud_provider]
        else:

            events_query = events_query % partitions[0]
            events_query += where_less_than_90 % Persistence.get_date(cloud_provider)[cloud_provider]
        return execute_sql(events_query).fetchall(), partitions

    except IndexError:
        return False, False


def execute_sql(sql_statement):

    conn = pyodbc.connect('Driver={SQL Server};' + DatabaseConnection.get_connection())
    cursor = conn.cursor()
    return cursor.execute(sql_statement)


def execute_policy_events(partition, row):
    return execute_sql(
        'SELECT * FROM [wbsn-data-security].[dbo].[PA_EVENT_POLICIES_%s] where EVENT_ID = %s' % (partition, row))


def query_events(partition, row):
    pa_events_query = 'SELECT * FROM [wbsn-data-security].[dbo].[PA_EVENTS_%s] where ID = %s'
    return table_fields_by_name(pa_events_query % (partition, row))


def query_services(service_id):
    services_query = 'SELECT * FROM [wbsn-data-security].[dbo].[PA_RP_SERVICES] where ID = %s'
    return table_fields_by_name(services_query % service_id)


def query_users(source_id):
    users_query = 'SELECT * FROM [wbsn-data-security].[dbo].[PA_MNG_USERS] where ID = %s'
    return table_fields_by_name(users_query % source_id)


def query_domains(id):
    query = 'SELECT * FROM [wbsn-data-security].[dbo].[PA_DOMAINS] WHERE ID = %s'
    return table_fields_by_name(query % id)


def query_destinations_users(partition, id):
    users_query = 'SELECT *  FROM [wbsn-data-security].[dbo].[PA_EVENT_DESTINATIONS_%s] where event_id = %s'
    destinations = table_fields_by_name(users_query % (partition, id))

    destinations_list = []

    for i in range(destinations.__len__()):
        destinations_list.append(query_users(destinations[i].USER_ID))

    return destinations_list


def query_policy_categories(id):
    query = 'SELECT * FROM [wbsn-data-security].[dbo].[PA_POLICY_CATEGORIES] where id = %s'
    return table_fields_by_name(query % id)


def super_call():
    test1 = '''SELECT dbo.PA_EVENTS_20191106.ID, dbo.PA_EVENT_POLICIES_20191106.ID AS EVENT_POLICY_ID, 
    dbo.PA_EVENTS_20191106.INSERT_DATE, dbo.PA_EVENTS_20191106.SUBJECT, dbo.PA_RP_SERVICES.PROTOCOL_ID, 
    dbo.PA_DOMAINS.NAME, dbo.PA_MNG_USERS.IP, PA_MNG_USERS_1.IP AS USER_DOMAINS_ID, PA_MNG_USERS_1.PORT as 
    USERS_1_PORT, dbo.PA_MNG_USERS.PORT AS USERS_PORT, dbo.PA_EVENT_DESTINATIONS_20191106.EVENT_ID, 
    dbo.PA_MNG_USERS.DOMAIN_ID AS USERS_DOMAIN_ID, PA_MNG_USERS_1.DOMAIN_ID AS USERS_1_DOMAIN_ID, 
    dbo.PA_EVENTS_20191106.EXTERNAL_ID, dbo.PA_RP_SERVICES.CHANNEL_NAME, dbo.PA_RP_SERVICES.AGENT_NAME, 
    dbo.PA_POLICY_CATEGORIES.NAME AS Expr4, dbo.PA_MNG_USERS.COMMON_NAME, dbo.PA_MNG_USERS.LOGIN_NAME,  
    dbo.PA_MNG_USERS.FULL_NAME, dbo.PA_MNG_USERS.EMAIL, PA_MNG_USERS_1.COMMON_NAME AS Expr5, 
    PA_MNG_USERS_1.LOGIN_NAME AS Expr6, PA_MNG_USERS_1.FULL_NAME AS Expr7, PA_MNG_USERS_1.EMAIL AS Expr8, 
    PA_MNG_USERS_1.EXTRA_DATA, dbo.PA_MNG_USERS.EXTRA_DATA AS Expr9, PA_MNG_USERS_1.HOSTNAME, 
    dbo.PA_MNG_USERS.HOSTNAME AS Expr10,  dbo.PA_EVENT_POLICIES_20191106.POLICY_CATEGORY_ID, 
    dbo.PA_EVENT_POLICIES_20191106.SEVERITY FROM dbo.PA_EVENTS_20191106 INNER JOIN dbo.PA_EVENT_POLICIES_20191106 ON 
    dbo.PA_EVENTS_20191106.ID = dbo.PA_EVENT_POLICIES_20191106.EVENT_ID INNER JOIN dbo.PA_RP_SERVICES ON 
    dbo.PA_EVENTS_20191106.SERVICE_ID = dbo.PA_RP_SERVICES.ID INNER JOIN dbo.PA_EVENT_DESTINATIONS_20191106 ON 
    dbo.PA_EVENTS_20191106.ID = dbo.PA_EVENT_DESTINATIONS_20191106.EVENT_ID INNER JOIN dbo.PA_RP_POLICY_NAMES ON 
    dbo.PA_EVENT_POLICIES_20191106.POLICY_NAME_ID = dbo.PA_RP_POLICY_NAMES.ID INNER JOIN dbo.PA_MNG_USERS ON 
    dbo.PA_EVENT_DESTINATIONS_20191106.USER_ID = dbo.PA_MNG_USERS.ID INNER JOIN dbo.PA_DOMAINS ON 
    dbo.PA_MNG_USERS.DOMAIN_ID = dbo.PA_DOMAINS.ID INNER JOIN dbo.PA_POLICY_CATEGORIES ON 
    dbo.PA_EVENT_POLICIES_20191106.POLICY_CATEGORY_ID = dbo.PA_POLICY_CATEGORIES.ID LEFT OUTER JOIN dbo.PA_MNG_USERS 
    AS PA_MNG_USERS_1 ON dbo.PA_DOMAINS.ID = PA_MNG_USERS_1.DOMAIN_ID AND dbo.PA_EVENTS_20191106.SOURCE_ID = 
    dbo.PA_MNG_USERS.ID'''
