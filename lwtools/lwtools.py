import json
import requests
import urllib
import datetime
import urllib.parse
import jwt
import boto3
import base64
from botocore.exceptions import ClientError


def get_jwt(lw_server_id, secret_key):
    timestamp = datetime.datetime.now().timestamp()
    jwt_token = jwt.encode(
        {
            "iss": lw_server_id,
            "iat": timestamp,
            "exp": timestamp + 3600
        },
        secret_key,
        algorithm="RS256")
    return jwt_token


def get_lw_token(secret_dic):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    form_data = {
        "grant_type": urllib.parse.quote("urn:ietf:params:oauth:grant-type:jwt-bearer"),
        "assertion": get_jwt(secret_dic['LineworksServerId'], secret_dic['LineworksSecretKey'])
    }
    r = requests.post(url='https://authapi.worksmobile.com/b/' + secret_dic['LineworksApiId'] + '/server/token',
                      data=form_data,
                      headers=headers)
    body = json.loads(r.text)
    return body["access_token"]


def get_lw_headers(secret_dic):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'consumerKey': secret_dic['LineworksConsumerKey'],
        'Authorization': ('Bearer %s' % get_lw_token(secret_dic))
    }
    return headers


def post_lw_room(secret_dic, headers, bot_id, post_str, room_id):
    payload = {
        'roomId': room_id,
        'content': {
            'type': 'text',
            'text': post_str
        }
    }
    return post_lw_payload(secret_dic, headers, bot_id, payload)


def post_lw_user(secret_dic, headers, bot_id, post_str, account_id):
    payload = {
        'accountId': account_id,
        'content': {
            'type': 'text',
            'text': post_str
        }
    }
    return post_lw_payload(secret_dic, headers, bot_id, payload)


def post_lw_payload(secret_dic, headers, bot_id, payload):
    post_url = 'https://apis.worksmobile.com/r/' + secret_dic[
        'LineworksApiId'] + '/message/v1/bot/' + bot_id + '/message/push'

    result = requests.post(post_url, data=json.dumps(payload), headers=headers)
    return result.status_code


def push_lw_calendar(secret_dic, headers, account_id, calendar_id, ical):
    post_url = 'https://apis.worksmobile.com/r/' + secret_dic[
        'LineworksApiId'] + '/calendar/v1/' + account_id + '/calendars/' + calendar_id + '/events'

    body = {
        "ical": ical
    }

    result = requests.post(post_url, headers=headers, data=json.dumps(body))
    return result.status_code


def create_room_with_bot(secret_dic, headers, bot_id, title, users, msg):
    post_url = 'https://apis.worksmobile.com/r/' + secret_dic['LineworksApiId'] + '/message/v1/bot/' + bot_id + '/room'
    payload = {
        'accountIds': users,
        'title': title
    }
    result = requests.post(post_url, data=json.dumps(payload), headers=headers)
    post_lw_room(secret_dic, headers, bot_id, msg, json.loads(result.text)['roomId'])
    return result.status_code


def get_secret_string(secret_id):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return secret
