import requests
import json

cloud_url = 'https://uscloud.experitest.com'
end_point = '/api/v1/devices'

cloud_url_and_api_end_point = cloud_url + end_point


def get_device_id(serial_number):
    # GET - /api/v1/devices?query=@serialnumber=serial_number
    # Bearer Auth Header
    # content-type application/json
    end_url = cloud_url_and_api_end_point + "?query=@serialnumber='" + serial_number + "'"

    headers = {
        'Authorization': 'Bearer eyJ4cC51Ijo3MzU0MjQsInhwLnAiOjIsInhwLm0iOiJNVFUzT0RZd016ZzFOek16TVEiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE4OTM5NjM4NTcsImlzcyI6ImNvbS5leHBlcml0ZXN0In0.GP0hK0o0j2WEKt-J0aXsVbu1tmt-PhWUryqluokszJk',
        'Content-Type': 'application/json'
    }

    response = requests.request('GET', end_url, headers=headers, verify=False)

    if response.status_code == 200:
        print('Successfully removed all device tags from device, response output: %s' % response.text)
        device_id = get_json_value_from_response_content('id', response.content)
    else:
        print('Unable to remove device tags from device, response output: %s' % response.text)

    return device_id

    # device_id = get_json_value_from_response_content('id', response.content)
    # return device_id


def remove_all_device_tags(device_id):
    # DELETE - /api/v1/devices/{id}/tags
    # Bearer Auth Header
    # content-type application/json
    end_url = cloud_url_and_api_end_point + '/' + device_id + '/tags'

    headers = {
        'Authorization': 'Bearer eyJ4cC51Ijo3MzU0MjQsInhwLnAiOjIsInhwLm0iOiJNVFUzT0RZd016ZzFOek16TVEiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE4OTM5NjM4NTcsImlzcyI6ImNvbS5leHBlcml0ZXN0In0.GP0hK0o0j2WEKt-J0aXsVbu1tmt-PhWUryqluokszJk',
        'Content-Type': 'application/json'
    }

    # response = requests.request('DELETE', end_url, headers=get_headers(), verify=False)
    response = requests.request('DELETE', end_url, headers=headers, verify=False)

    if response.status_code == 200:
        print('Successfully removed all device tags from device, response output: %s' % response.text)
    else:
        print('Unable to remove device tags from device, response output: %s' % response.text)

    return response


def add_device_tag(device_id, tag_value):
    # PUT - /api/v1/devices/{id}/tags/{tag_value}
    # Bearer Auth Header
    # content-type application/json
    end_url = cloud_url_and_api_end_point + '/' + device_id + '/tags/' + tag_value

    headers = {
        'Authorization': 'Bearer eyJ4cC51Ijo3MzU0MjQsInhwLnAiOjIsInhwLm0iOiJNVFUzT0RZd016ZzFOek16TVEiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE4OTM5NjM4NTcsImlzcyI6ImNvbS5leHBlcml0ZXN0In0.GP0hK0o0j2WEKt-J0aXsVbu1tmt-PhWUryqluokszJk',
        'Content-Type': 'application/json'
    }

    response = requests.request('PUT', end_url, headers=headers, verify=False)

    if response.status_code == 200:
        print('Successfully removed all device tags from device, response output: %s' % response.text)
    else:
        print('Unable to remove device tags from device, response output: %s' % response.text)

    return response


def finish_cleanup_state(uid, status):
    # POST - /api/v1/cleanup-finish?deviceId=uid&status=status
    # Bearer Auth Header
    return 0


def get_headers():
    headers = {
        'Authorization': 'Bearer eyJ4cC51Ijo3MzU0MjQsInhwLnAiOjIsInhwLm0iOiJNVFUzT0RZd016ZzFOek16TVEiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE4OTM5NjM4NTcsImlzcyI6ImNvbS5leHBlcml0ZXN0In0.GP0hK0o0j2WEKt-J0aXsVbu1tmt-PhWUryqluokszJk',
        'Content-Type': 'application/json'
    }
    return headers


def get_json_value_from_response_content(value, response_content):
    data = json.loads(response_content)
    return_value = data['data'][0]['%s' % value]
    return return_value

