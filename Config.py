import json
from pathlib import Path
from PasswordEncryption.PasswordHandler import decrypt_password, encrypt_password

secure_key = ''


def get_key():
    return secure_key


def set_key(key):
    global secure_key
    secure_key = key


def get_db_config():
    with open('Config.json', 'r') as jsonFile:
        parsed_json = json.load(jsonFile)
    return parsed_json


def set_db_config(config):
    with open('Config.json', 'w') as jsonFile:
        json.dump(config, jsonFile, indent=4)


class DatabaseConnection:

    @staticmethod
    def save_password(password, username):
        key, encrypted_pwd = encrypt_password(password)
        config = get_db_config()
        config["Database_Connection"]['PWD'] = encrypted_pwd
        config["Database_Connection"]['UID'] = username
        set_db_config(config)
        set_key(key)
        return key

    @staticmethod
    def get_connection():
        with open('Config.json', 'r') as jsonFile:
            parsed_json = json.load(jsonFile)
            connection_string_list = parsed_json["Database_Connection"]

            if connection_string_list["Trusted_Connection"] == 'yes':
                del connection_string_list['UID']
                del connection_string_list['PWD']
                if connection_string_list['Server'] == "" or connection_string_list['Database'] == "":
                    return 'none'
            else:
                del connection_string_list['Trusted_Connection']
                connection_string_list['PWD'] = decrypt_password(secure_key, connection_string_list['PWD']).decode(
                    "utf-8")
                if connection_string_list['Server'] == "" or connection_string_list['Database'] == "" or \
                        connection_string_list['UID'] == "" or connection_string_list['PWD'] == "":
                    return 'none'
            connection_string = ''
            for i in connection_string_list:
                str_of_con = str(i)
                str_of_con += '='
                str_of_con += connection_string_list[i]
                str_of_con += ';'
                connection_string += str_of_con
        return connection_string


class Persistence:
    @staticmethod
    def get_date(cloud_provider):
        if cloud_provider == 'AzureUpdateDate':
            with open('Resources/azureDate.json', 'r') as jsonFile:
                parsed_json = json.load(jsonFile)
        elif cloud_provider == 'AWSUpdateDate':
            with open('Resources/AWSDate.json', 'r') as jsonFile:
                parsed_json = json.load(jsonFile)
        return parsed_json

    @staticmethod
    def set_date(date, cloud_provider):
        data = Persistence.get_date(cloud_provider)

        data[cloud_provider] = date
        if cloud_provider == 'AzureUpdateDate':
            with open("Resources/azureDate.json", "w") as jsonFile:
                json.dump(data, jsonFile)
        elif cloud_provider == 'AWSUpdateDate':
            with open("Resources/AWSDate.json", "w") as jsonFile:
                json.dump(data, jsonFile)

    @staticmethod
    def get_arn():
        with open('Resources/InsightARN.json', 'r') as jsonFile:
            parsed_json = json.load(jsonFile)
        return parsed_json

    @staticmethod
    def set_arn(arn, key):
        data = Persistence.get_arn()

        data["ARN"][key] = arn

        with open("Resources/InsightARN.json", "w") as jsonFile:
            json.dump(data, jsonFile)


class Configurations:
    @staticmethod
    def get_configurations():
        with open('Config.json', 'r') as f:
            parsed_json = json.load(f)
        f.close()
        return parsed_json

    @staticmethod
    def get_arn():
        region = ''
        with open('Config.json', 'r') as f:
            parsed_json = json.load(f)
            region = parsed_json['region_name']
        f.close()
        return f'arn:aws:securityhub:{region}:365761988620:product/forcepoint/forcepoint-dlp'


class Insights:
    @staticmethod
    def get_keys():
        my_file = Path("./Resources/Insights.json")
        if my_file.is_file():
            with open('Resources/Insights.json', 'r') as f:
                parsed_json = json.load(f)
            f.close()
            return parsed_json
