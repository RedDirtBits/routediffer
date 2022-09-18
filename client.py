import logging
import sys
import os
from dataclasses import dataclass, field
from netmiko import ConnLogOnly
from dotenv import load_dotenv


@dataclass
class LoginCredentials:
    """
     A dataclass that pulls a set of credentials from a user provided .env
     file containing a prefix that uniquely identifies a particular set of
     credentials over another
    """

    load_dotenv()

    credential_id: str
    username: str = field(default="")
    password: str = field(default="")
    enable: str = field(default="")

    def __post_init__(self):

        self.username = os.environ.get(f"{self.credential_id}_username")
        self.password = os.environ.get(f"{self.credential_id}_password")
        self.enable = os.environ.get(f"{self.credential_id}_enable")


class SSHClient:
    """
     SSHClient summary:

    Args:
        hostname (str):
            The hostname or IP address of the network device being logged into

        credential_id (str):
            The credential_id is a prefix for the user provided .env file that
            uniquely identifies a set of credentials out of all that may exist
            within the .env file

            This allows for flexibility for when one may work in different environments
            where SSH login credentials may be different.  For example, testing,
            production, etc.

            This assumes the .env file has been written so that all credentials are written
            in a uniform manner using a prefix to identify the particular credentials
            needed.

            For example: testing_username, testing_password, testing_secret

            In this case, the user would set the credential_id argument to "testing"

        platform_id (str):
            The Netmiko platform being connected to.  Can be cisco_ios for IOS
            devices, cisco_nxos for Nexus devices, cisco_telnet for when using
            Telnet, etc.
    """

    def __init__(self, hostname: str, credential_id: str, platform_id: str) -> None:

        self.hostname = hostname
        self.credential_id = credential_id
        self.platform_id = platform_id
        self.session = None

        self.credentials = LoginCredentials(self.credential_id)

        self.ssh_profile = {
            "device_type": self.platform_id,
            "host": self.hostname,
            "username": self.credentials.username,
            "password": self.credentials.password,
            "secret": self.credentials.enable
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
            return sys.exit(f"Unable To Log in to: {self.hostname}")
        else:
            self.device_hostname = self.session.find_prompt()[:-1]

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
