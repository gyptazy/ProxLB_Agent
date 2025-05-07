"""
The Client class provides the functions for interacting with the ProxLB API server.
"""

__author__ = "Florian Paul Azim Hoberg <gyptazy>"
__copyright__ = "Copyright (C) 2025 Florian Paul Azim Hoberg (@gyptazy)"
__license__ = "GPL-3.0"


import urllib
import urllib.request
import json
import utils.version
from utils.logger import SystemdLogger
from typing import Dict, Any

logger = SystemdLogger()


class Client:
    """
    The DPM class provides the agent support for dynamic power management in ProxLB.

    Methods:
        __init__():
            Initializes the general Helper class.

        get_uuid_string() -> str:
            Generates a random uuid and returns it as a string.

        log_node_metrics(proxlb_data: Dict[str, Any], init: bool = True) -> None:
            Logs the memory, CPU, and disk usage metrics of nodes in the provided proxlb_data dictionary.

        get_version(print_version: bool = False) -> None:
            Returns the current version of ProxLB and optionally prints it to stdout.

        get_daemon_mode(proxlb_config: Dict[str, Any]) -> None:
            Checks if the daemon mode is active and handles the scheduling accordingly.
    """
    def __init__(self):
        """
        Initializes the general DPM class.
        """

    @staticmethod
    def get(uri: str, show_errors=True) -> str:
        """
        Receives the content of a GET request from a given URI.

        Parameters:
            uri (str): The URI to get the content from.

        Returns:
            str: The response content.
        """
        logger.debug("Starting: http_client_get.")
        http_charset = "utf-8"
        http_headers = {
            "User-Agent": f"ProxLB API client/{utils.version.__version__}",
        }
        http_request = urllib.request.Request(uri, headers=http_headers, method="GET")

        try:
            logger.debug(f"Get http client information from {uri}.")
            with urllib.request.urlopen(http_request) as response:
                http_client_content = response.read().decode(http_charset)
                return http_client_content
        except urllib.error.HTTPError as e:
            if show_errors:
                logger.error(f"HTTP error: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            if show_errors:
                logger.error(f"URL error: {e.reason}")
        logger.debug("Finished: http_client_get.")

    @staticmethod
    def post(proxlb_agent_config, uri: str, data, show_errors=True) -> str:
        """
        Sends a POST request to a given URI with the provided data.

        Parameters:
            uri (str): The URI to send the POST request to.
            data: The data to send in the request body.
            show_errors (bool): Whether to show errors in logs.

        Returns:
            str: The response content as a string.
        """
        logger.debug("Starting: http_client_post.")
        http_charset = "utf-8"

        token = proxlb_agent_config.get('proxlb_api', {}).get('token', '')
        http_headers = {
            "User-Agent": f"ProxLB API client/{utils.version.__version__}",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        request_data = json.dumps(data).encode(http_charset)
        request = urllib.request.Request(uri, data=request_data, headers=http_headers, method="POST")

        try:
            logger.debug(f"Posting to {uri} with data: {data}")
            with urllib.request.urlopen(request) as response:
                http_client_content = response.read().decode(http_charset)
                logger.debug("Finished: http_client_post.")
                return http_client_content
        except urllib.error.HTTPError as e:
            if show_errors:
                logger.error(f"HTTP error: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            if show_errors:
                logger.error(f"URL error: {e.reason}")

        logger.debug("Finished: http_client_post with error.")