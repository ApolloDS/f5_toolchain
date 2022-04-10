""" F5 DO send comand """

import click
import sys
import logging
import json
import npyscreen
import curses
import requests
from requests.auth import HTTPBasicAuth

@click.command()
@click.pass_obj
def send(obj):
    """Send DO JSON file to F5"""

    API_ENDPOINT = f'https://{obj.hostname}/mgmt/shared/declarative-onboarding'

    logging.debug(f"info subcommand obj: {vars(obj)}")

    # disable cert warnings
    requests.packages.urllib3.disable_warnings()

    # curses initialization, needed to init size of window
    curses.initscr()

    filepath = npyscreen.selectFile()
    f = open(filepath)
    filedata = json.load(f)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


    # Return the terminal to its original state
    curses.nocbreak ()
    curses.echo ()
    curses.curs_set (1)
    curses.endwin ()

    if obj.hostname and obj.password:
        try:
            logging.info(f"connecting to {obj.hostname}")
            response = requests.post(
                API_ENDPOINT, verify=False,
                data=json.dumps(filedata),
                headers=headers,
                auth=HTTPBasicAuth(
                    obj.username, obj.password
                )
            )
            logging.debug(response)
            if response.status_code == 401:
                logging.error('wrong username or password!')
                sys.exit(1)
        except Exception as e:
            logging.error('send command: {}'.format(e))
            sys.exit(1)
    else:
        logging.error('please specifiy username and password!')
        sys.exit(1)
