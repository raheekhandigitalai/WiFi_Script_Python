import requests
import json
import configparser

from Helper import logger

config = configparser.ConfigParser()
config.read('config.properties')

cloud_url = 'https://uscloud.experitest.com'
end_point = '/api/v1/devices'

cloud_url_and_api_end_point = cloud_url + end_point


def get_device_id(serial_number):
    end_url = cloud_url_and_api_end_point + "?query=@serialnumber='" + serial_number + "'"

    headers = {
        'Authorization': 'Bearer %s' % config.get('seetest_authorization', 'access_key_admin'),
        'Content-Type': 'application/json'
    }

    response = requests.request('GET', end_url, headers=headers, verify=False)

    device_id = get_json_value_from_response_content('id', response.content)
    return device_id


def remove_all_device_tags(device_id):
    end_url = cloud_url_and_api_end_point + '/' + device_id + '/tags'

    headers = {
        'Authorization': 'Bearer %s' % config.get('seetest_authorization', 'access_key_admin'),
        'Content-Type': 'application/json'
    }

    response = requests.request('DELETE', end_url, headers=headers, verify=False)

    if response.status_code == 200:
        logger('Python Script (function: remove_all_device_tags) - Successfully removed all device tags from device, '
               'response output: %s' % response.text)
    else:
        logger('Python Script (function: remove_all_device_tags) - Unable to remove device tags from device, '
               'response output: %s' % response.text)

    return response


def add_device_tag(device_id, tag_value):
    end_url = cloud_url_and_api_end_point + '/' + device_id + '/tags/' + tag_value

    headers = {
        'Authorization': 'Bearer %s' % config.get('seetest_authorization', 'access_key_admin'),
        'Content-Type': 'application/json'
    }

    response = requests.request('PUT', end_url, headers=headers, verify=False)

    if response.status_code == 200:
        logger('Python Script (function: add_device_tag) - Successfully added device tag to device, response output: %s' % response.text)
        logger('Python Script (function: add_device_tag) - Device Tag Added: %s' % tag_value)
    else:
        logger('Python Script (function: add_device_tag) - Unable to add device tag to device, response output: %s' % response.text)

    return response


def finish_cleanup_state(uid, status):
    end_url = 'https://uscloud.experitest.com/api/v1/cleanup-finish?deviceId=' + str(uid) + '&status=' + str(status)

    headers = {
        'Authorization': 'Bearer %s' % config.get('seetest_authorization', 'access_key_cleanup'),
        'Content-Type': 'application/json'
    }

    response = requests.request('POST', end_url, headers=headers, verify=False)

    if response.status_code == 200:
        logger('Python Script (function: finish_cleanup_state) - Successfully finished Cleanup State: %s' % response.text)
    else:
        logger('Python Script (function: finish_cleanup_state) - Unable to finish Cleanup State: %s' % response.text)

    return response


def get_json_value_from_response_content(value, response_content):
    data = json.loads(response_content)
    return_value = data['data'][0]['%s' % value]
    return return_value

