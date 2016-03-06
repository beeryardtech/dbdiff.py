#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox import rest as dbrest
import logging

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__ = logging.getLogger(__name__)


def build_client(config, auth_token = None, force_new = True):
    """
    Builds the Dropbox Client. Also update the config object.

    If the client is already available just return that copy. Use `force_new` to
    create a new instance.
    """
    if config.get("client") and not force_new:
        return (config.get("client"), config)

    if auth_token:
        pass

    elif not auth_token and config.get("auth_token"):
        __log__.debug("Using auth_token from config")
        auth_token = config.get("auth_token")

    elif not auth_token and not config.get("auth_token"):
        __log__.debug("No auth_token available. Starting auth flow")
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
    __log__.info("Auth code not provided or in config! {}".format(config))

    auth_flow = DropboxOAuth2FlowNoRedirect(
        config.get("app_key"),
        config.get("app_secret")
    )

    # Get the auth stuff.
    auth_url = auth_flow.start()
    auth_code = ask_for_auth_code_or_exit(auth_url, config)
    auth_token, config = try_finish_auth_flow(auth_code, auth_url, config)

    # Put the information on a copy of config object
    configClone = config.copy()
    configClone.update({
        "auth_flow": auth_flow,
        "auth_url": auth_url,
    })

    return (auth_token, configClone)


def ask_for_auth_code_or_exit(auth_url, config):
    """
    First log instructions on how to get auth_code.

    If `config.input_disabled` is False, then ask the user for the auth_code. Otherwise,
    log instructions on how to update config file and exit program.
    """
    log_auth_url(auth_url)

    if not config.get("input_disabled"):
        __log__.info("Input is disabled. Update config file with the auth code!")
        raise AuthInputDisabled('Input Disabled')

    else:
        auth_code = raw_input('Auth Code: ').strip()

    return auth_code


def log_auth_url(auth_url):
    __log__.warn("- Go to this url: {}".format(auth_url))
    __log__.warn("- Click 'Allow' (you might have to log in first).")
    __log__.warn("- Copy the auth_code into config file and into input")

    return


def try_finish_auth_flow(auth_flow, auth_code, auth_url, config):
    """
    Tries to crun the `auth_flow.finish()` with the given `auth_code`. If that fails
    with a 400 error, then ask try to ask the user for a new `auth_code` (if `input_disabled`
    is not true). If any other error, return with `None`.
    """
    try:
        auth_token, user_id = auth_flow.finish(auth_code)

    except dbrest.ErrorResponse as err:
        if(err.status == 400):
            __log__.warn("Got a 400!")

            # Get a new auth code and try again.
            auth_code = ask_for_auth_code_or_exit(auth_url, config)
            return try_finish_auth_flow(auth_flow, auth_code, auth_url, config)

        else:
            __log__.exception("Falied to finish auth! {}".format(err.body))
            return (None, config)

    configClone = config.copy()
    configClone.update({
        "auth_code": auth_code,
        "auth_token": auth_token,
        "user_id": user_id,
    })

    return (auth_token, configClone)


class AuthInputDisabled(Exception):
    """
    Expection for when inputs (such as raw_input) is unavailable. The caller should handle this.
    Acts similar to a call to `sys.exit()`.
    """
    pass


if __name__ == '__main__':
    pass
