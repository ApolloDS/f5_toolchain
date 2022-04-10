""" F5 DO status comand """

import click
import sys
import logging
import json
import requests
from requests.auth import HTTPBasicAuth

@click.command()
@click.pass_obj
def status(obj):
    """Get status of F5 DO"""

    API_ENDPOINT = f'https://{obj.hostname}/mgmt/shared/declarative-onboarding'

    logging.debug(f"info subcommand obj: {vars(obj)}")

    # disable cert warnings
    requests.packages.urllib3.disable_warnings()

    if obj.hostname and obj.password:
        try:
            logging.info(f"connecting to {obj.hostname}")
            response = requests.get(
                API_ENDPOINT, verify=False,
                auth=HTTPBasicAuth(
                    obj.username, obj.password
                )
            )
            logging.debug(f'status code: {response.status_code}')
            if response.status_code == 401:
                logging.error('wrong username or password!')
                sys.exit(1)
            elif response.status_code in [200, 201, 202, 204, 207]:
                print('DO is up and running...')
                sys.exit()
            elif response.status_code == 422:
                # extract text from JSON
                text = response.text
                data = json.loads(text)
                logging.debug(data)

                # check for errors
                errors = _get_errors_from_response(data)
                if errors:
                    message = '{0}'.format('. '.join(errors))
                    logging.error(message)
                    sys.exit(1)
        except Exception as e:
            logging.error('status command: {}'.format(e))
            sys.exit(1)
    else:
        logging.error('please specifiy username and password!')
        sys.exit(1)

def _get_errors_from_response(message):
    results = []
    if 'message' in message and message['message'] == 'invalid config - rolled back':
        results.append(message['message'])
    if 'errors' in message:
        results += message['errors']
    return results