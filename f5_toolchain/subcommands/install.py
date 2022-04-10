""" F5 DO install comand """

import click
import sys
import logging
import npyscreen
import curses
from bigrest.bigip import BIGIP
from pathlib import Path

@click.command()
@click.pass_obj
def install(obj):
    """Installing the F5 Tool Chain RPM files"""

    # init bigrest
    device = BIGIP(obj.hostname, obj.username, obj.password)

    # curses initialization, needed to init size of window
    curses.initscr()

    selected_file = npyscreen.selectFile()

    # Return the terminal to its original state
    curses.nocbreak ()
    curses.echo ()
    curses.curs_set (1)
    curses.endwin ()

    logging.debug(f"info subcommand obj: {vars(obj)}")

    # disable cert warning
    #requests.packages.urllib3.disable_warnings()

    if obj.hostname:
        try:
            logging.info(f'uploading {selected_file} to {obj.hostname}')
            response = upload_file(device, selected_file)
            if response:
                print(f'Upload of file {selected_file} was successful!')
            
            install = install_package(device, selected_file)
            if install:
                print('Installation of uploaded file was successful!')

            verify = verify_package(device, selected_file)
            if verify:
                print('Verify of uploaded file was successful!')

        except Exception as e:
            logging.error("status command: {}".format(e))
            sys.exit(1)

def upload_file(obj, filename):
    try:
        obj.upload(f'/mgmt/shared/file-transfer/uploads/', filename)
    except Exception as e:
        logging.error(f'Failed to upload the component due to {type(e).__name__}:')
        logging.error(f'{e}')
        sys.exit(1)
    return True

def install_package(obj, filename):
    try:
        data = {"operation": "INSTALL", "packageFilePath": f"/var/config/rest/downloads/{Path(filename).name}"}
        obj.command("/mgmt/shared/iapp/package-management-tasks", data)
    except Exception as e:
        logging.error(f"Failed to install the component due to {type(e).__name__}:")
        logging.error(f"{e}")
        sys.exit()
    return True

def verify_package(obj, filename):
    #component = Path(filename).name
    if "f5-declarative-onboarding" in filename:
        try:
            result = obj.load("/mgmt/shared/declarative-onboarding/info")
            if result.properties[0].get('version') in filename:
                return True
            else:
                return False
        except RESTAPIError:
            return False
    elif "f5-appsvcs" in filename:
        try:
            result = obj.load("/mgmt/shared/appsvcs/info")
            if result.properties.get('version') in filename:
                return True
            else:
                return False
        except RESTAPIError:
            return False
    elif "f5-telemetry" in filename:
        try:
            result = obj.load("/mgmt/shared/telemetry/info")
            if result.properties.get('version') in filename:
                return True
            else:
                return False
        except RESTAPIError:
            return False
    else:
        return False