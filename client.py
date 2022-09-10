import logging
import sys
import os
from dotenv import load_dotenv
from netmiko import ConnLogOnly


class SSHClient:
    """
     SSHClient summary:

    Args:
        hostname (str):
            The hostname or IP address of the network device being logged into

        profile (str):
            The profile is a prefix for the user provided .env file which is loaded
            and read by the third-party library python-dotenv.  The load_dotenv()
            method is initialized as part of the class init.

            This allows for flexibility for when one may work in different environments
            where SSH login credentials may be different.  For example, testing,
            production, etc.

            This assumes the .env file has been written so that all credentials are written
            in a uniform manner using a uniform prefix to uniquely identify the environment

            Example: testing_username, testing_password, testing_secret

            In this case, the user would set the profile argument to "testing"

        platform (str):
            The Netmiko platform being connected to.  Can be cisco_ios for IOS
            devices, cisco_nxos for Nexus devices, cisco_telnet for when using
            Telnet, etc.
    """

    def __init__(self, hostname: str, profile: str, platform: str) -> None:

        self.hostname = hostname
        self.profile = profile
        self.platform = platform
        self.session = None

        load_dotenv()

        self.ssh_profile = {
            "device_type": self.platform,
            "host": self.hostname,
            "username": os.environ.get(f"{self.profile}_username"),
            "password": os.environ.get(f"{self.profile}_password"),
            "secret": os.environ.get(f"{self.profile}_enable"),
        }

    def ssh_host_login(self):
        """
        ssh_host_login summary
            Uses Netmiko "ConnLogOnly" handler (not the typical "ConnectionHandler")
            to log into a network device.

        Returns:
            BaseConnection: The SSH log in session that can either be None or
            a netmiko_object if successfully logged in.  Exceptions are handled by
            default and logged to the default log file "netmiko.log"
        """

        self.session = ConnLogOnly(
            **self.ssh_profile,
            log_level=logging.INFO,
            )
        
        # make sure that we have logged into the device.  Check the connection
        # handler if this is encountered
        if self.session is None:
            sys.exit(f"Unable To Log in to: {self.hostname}")

        # in most cases, particularly in cases using TACACS, we will be dropped into
        # privileged EXEC mode on the device.  However, as a sanity check, let's make
        # sure and if not run enable to get there
        if not self.session.check_enable_mode():
            self.session.enable()

        return self.session

    def ssh_host_disconnect(self):
        """
        ssh_host_disconnect summary
            Disconnects from a Netmiko SSH session
        """

        self.session.disconnect()
