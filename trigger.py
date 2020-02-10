import os
import json
import requests


def trigger_build(branch):
    username = ''
    password = ''
    url = ''
    headers = {
        'X-Forwarded-User': '',
        'X-Forwarded-Groups': '',
    }
    payload = {
        'BRANCH': branch
    }
    r = requests.post(
        url,
        headers=headers,
        data=payload,
        auth=(username, password)
    )

    return r


def handler(event, context):
    if 'branch' in event['queryStringParameters'].keys():
        body = trigger_build(event['queryStringParameters'].get('branch'))

        if body.status_code == 201:
            return {
                'statusCode': 201,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps(
                    {
                        'status': f'The build for {event["queryStringParameters"].get("branch")} has been started.'
                    }
                )
            }
        else:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps(
                    {
                        'status': f'There was an error starting the build for {event["queryStringParameters"].get("branch")}.',
                        'status_code': body.status_code,
                        'error': body.content
                    }
                )
            }
