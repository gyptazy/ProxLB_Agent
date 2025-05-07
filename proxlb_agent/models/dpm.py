"""
The DPM class provides the agent support for dynamic power management in ProxLB.
"""

__author__ = "Florian Paul Azim Hoberg <gyptazy>"
__copyright__ = "Copyright (C) 2025 Florian Paul Azim Hoberg (@gyptazy)"
__license__ = "GPL-3.0"


from models.client import Client
from utils.helper import Helper
from utils.logger import SystemdLogger
from typing import Dict, Any

logger = SystemdLogger()


class DPM:
    """
    The DPM class provides the agent support for dynamic power management in ProxLB.

    Methods:
        __init__():
            Initializes the general Helper class.

        get_mac_address() -> str:
            Validates in ProxLB API if the MAC address is already registered and returns it.

        set_mac_address() -> str:
            Sets in ProxLB API the MAC address of an agent node.
    """
    def __init__(self):
        """
        Initializes the general DPM class.
        """

    @staticmethod
    def get_mac_address(proxlb_agent_config) -> str:
        """
        Generates a random uuid and returns it as a string.

        Args:
            None

        Returns:
            Str: Returns a random uuid as a string.
        """
        logger.debug("Starting: get_mac_address.")
        server = proxlb_agent_config.get('proxlb_api', {}).get('host', '')
        print(server)
        port = proxlb_agent_config.get('proxlb_api', {}).get('port', '')
        hostname = Helper.get_hostname()
        print(f"http://{server}:{port}/nodes/{hostname}")
        Client.get(f"http://{server}:{port}/nodes/{hostname}")
        logger.debug("Finished: get_mac_address.")

    @staticmethod
    def set_mac_address(proxlb_agent_config) -> str:
        """
        Generates a random uuid and returns it as a string.

        Args:
            None

        Returns:
            Str: Returns a random uuid as a string.
        """
        logger.debug("Starting: get_mac_address.")

        server = proxlb_agent_config.get('proxlb_api', {}).get('host', '')
        port = proxlb_agent_config.get('proxlb_api', {}).get('port', '')
        mac = proxlb_agent_config.get('dpm', {}).get('wol_mac', '')
        hostname = Helper.get_hostname()

        data = {
            "name": hostname,
            "wol_mac": mac,
            "mode_patch": False,
            "mode_dpm": False,
            "released": False,
            "processed": False
        }

        print(f"http://{server}:{port}/nodes/{hostname}")
        Client.post(proxlb_agent_config, f"http://{server}:{port}/nodes/{hostname}", data)
        logger.debug("Finished: get_mac_address.")