#!/usr/bin/env python

from os import environ
import click
import logging
import re
import importlib
from pathlib import Path

__author__ = """Peter Baumann"""
__email__ = 'petbau@linuxnet.ch'
__version__ = '1.0.0'

PLUGIN_FOLDER = Path('f5_toolchain/subcommands')

class F5Host(object):
    def __init__(self, hostname=None, username=None,
        password=None, verbose=None, debug=None) -> None:
        self.hostname = hostname
        self.username = username
        self.password = password
        self.verbose = verbose
        self.debug = debug

@click.group()
@click.version_option(__version__)
@click.pass_context # pass general options to command
@click.option(
    '-h',
    '--hostname',
    envvar='F5_TOOLCHAIN_HOSTNAME',
    required = True,
    help = (
        'The F5 hostname to connect to REST-API'
    )
)
@click.option(
    '-u',
    '--username',
    envvar='F5_TOOLCHAIN_USERNAME',
    default = 'admin',
    show_default = "current user",
    required = True,
    help = (
        'F5 BIG-IP username'
    )
)
@click.password_option(
    confirmation_prompt = False,
    envvar='F5_TOOLCHAIN_PASSWORD',
    prompt_required = True,
    hide_input = True,
    default = 'admin',
    help = (
        'F5 BIG-IP user password [prompted when not specified]'
    )
)
@click.option(
    '-v',
    '--verbose',
    is_flag = True,
    default = False,
    help = (
        'Enables VERBOSE mode.'
    )
)
@click.option(
    '-d',
    '--debug',
    is_flag = True,
    default = False,
    help = (
        'Enables DEBUG mode.'
    )
)

def entry_point(ctx, hostname, username, password, verbose, debug):

    """
    f5-toolchain is a tool that helps you to do declarative onboarding with F5 BIG-IP
    over REST-API.

    You need to specifiy the hostname, username and the password
    of the F5 device for the tool to work.

    For detailed help, try this: f5-toolchain help COMMAND
    """

    loglevel = None

    if verbose:
        loglevel = logging.INFO
    if debug:
        loglevel = logging.DEBUG

    # initialize logging
    logging.basicConfig(
        level = loglevel,
        force = True,
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt = '%d-%b-%y %H:%M:%S'
    )

    ctx.obj = F5Host(hostname, username, password, verbose, debug)

def add_subcommands(maincommand=entry_point):
    for modpath in PLUGIN_FOLDER.glob('*.py'):
        modname = re.sub(f'/', '.',  str(modpath)).rpartition('.py')[0]
        mod = importlib.import_module(modname)
        # filter out any things that aren't a click Command
        for attr in dir(mod):
            cmd = getattr(mod, attr)
            if callable(cmd) and type(cmd) is click.core.Command:
                maincommand.add_command(cmd)

def main():
    add_subcommands()
    logging.debug("test")
    entry_point()

if __name__ == '__main__':
    main()