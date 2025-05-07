"""
ProxLB Agent
"""

__author__ = "Florian Paul Azim Hoberg <gyptazy>"
__copyright__ = "Copyright (C) 2025 Florian Paul Azim Hoberg (@gyptazy)"
__license__ = "GPL-3.0"


import logging
from models.dpm import DPM
from utils.logger import SystemdLogger
from utils.cli_parser import CliParser
from utils.config_parser import ConfigParser
from utils.helper import Helper


def main():
    """
    ProxLB Agent main function
    """
    # Initialize logging handler
    logger = SystemdLogger(level=logging.INFO)

    # Parses arguments passed from the CLI
    cli_parser = CliParser()
    cli_args = cli_parser.parse_args()
    Helper.get_version(cli_args.version)

    # Parse ProxLB config file
    config_parser = ConfigParser(cli_args.config)
    proxlb_agent_config = config_parser.get_config()

    # Update log level from config and fallback to INFO if not defined
    logger.set_log_level(proxlb_agent_config.get('service', {}).get('log_level', 'INFO'))

    # Get own MAC address of management interface
    client_info = DPM.get_mac_address(proxlb_agent_config)
    print(client_info)

    if client_info is None:
        logger.error("Failed to get MAC address.")
        DPM.set_mac_address(proxlb_agent_config)

    logger.debug(f"Finished: __main__")


if __name__ == "__main__":
    main()
