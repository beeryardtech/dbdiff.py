#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import gettext
import logging
import os
from os.path import dirname, realpath # for library path manipulation
import sys
from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox import rest as dbrest

# For translations



__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__  = logging.getLogger(__name__)

def build_client(config, auth_token = None):
    """
    Builds the Dropbox Client
    """
    if auth_token:
        pass

    elif not auth_token and config.get("auth_token"):
        auth_token = config.get("auth_token")

    elif not auth_token and not config.get("auth_token"):
        auth_token, config = start_auth_flow(config)

    __log__.debug("Creating the dropbox client!")
    client = DropboxClient(auth_token)
    __log__.debug("Successfully created client!")

    # Put the information on a copy of config object
    configClone = config.copy()
    configClone.update({
        "auth_token": auth_token,
        "client": client,
    })

    return (client, configClone)

def start_auth_flow(config):
    """
    Create the OAuth2 flow. This allows the user to get auth_token
    """
    __log__.info("Auth code not provided or in config!")

    auth_flow = DropboxOAuth2FlowNoRedirect(
        config.get("app_key"),
        config.get("app_secret")
    )

    auth_url = auth_flow.start()
    auth_code = ask_for_auth_code(auth_url)

    try:
        auth_token, user_id = auth_flow.finish(auth_code)

    except dbrest.ErrorResponse as err:
        if(err.status == 400):
            __log__.warn("Got a 400!")

            # Get auth code and try again.
            auth_code = ask_for_auth_code(auth_url)
            return start_auth_flow(config)

        else:
            __log__.exception("Falied to finish auth! {}".format(err.body))
            return (None, config)

    # Put the information on a copy of config object
    configClone = config.copy()
    configClone.update({
        "auth_code": auth_code,
        "auth_flow": auth_flow,
        "user_id": user_id,
    })

    return (auth_token, configClone)


def ask_for_auth_code(auth_url):
    log_auth_url(auth_url)
    auth_code = raw_input('Auth Code: ').strip()

    return auth_code

def log_auth_url(auth_url):
    __log__.warn("- Go to this url: {}".format(auth_url))
    __log__.warn("- Click 'Allow' (you might have to log in first).")
    __log__.warn("- Copy the auth_code into config file and into input")

    return

if __name__ == '__main__':
    pass
