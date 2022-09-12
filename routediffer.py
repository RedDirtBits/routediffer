
import json
from paths import Paths


def get_routing_table(ip_address: str, credential_id: str, platform: str):
    """
    get_routing_table summary
        Logs into a core switch/router and gets the current routing table.  On the initial run
        it checks if the routes have already been written to a file.  If that has not taken place
        the file is created and the routes saved as a source of truth.  Otherwise, the routes in
        TextFSM structured format are returned for use elsewhere.

    Args:
        ip_address (str): The IP address of the core switch/router to be logged into.  This can
        also be a hostname but note that the hostname should be resolvable to an IP address.

        credential_id (str): This is the prefix used to identify the login credential set in the
        user provided .env file.  Assuming, for example your username was test_username, the 
        credential ID would be "test".  This assumes that all credentials follow this patter.
        Example: test_username, test_password, test_secret, etc.

        platform (str): The Netmiko platform identifier.  Can be "cisco_ios" for IOS based
        devices, "cisco_nexus" for Nexus devices, etc.

    Raises:
        ValueError: A ValueError is returned if any the arguments, "ip_address", "credential_id"
        or "platform" are missing

    Returns:
        dict: The device routing table in TextFSM structured format if the source of truth file
        has already been created
    """

    # run the import statements from within the function as it makes it easier to work with the log in
    from client import SSHClient
    from ciscocmds import CiscoCommands

    # let's make sure the required information has been provided and if not try and gracefully handle that
    if not ip_address or not credential_id or not platform:

        raise ValueError("IP Address, Credential ID and Platform Type are required")
    
    else:

        # if there were no exceptions, everything needed should be preset therefore proceed with
        # the log in to get the routing table
        ssh_client = SSHClient(hostname=ip_address, profile=credential_id, platform=platform)
        ssh_client.ssh_host_login()

        routing_table = ssh_client.session.send_command(
            CiscoCommands.show_routes(), use_textfsm=True, strip_prompt=True, strip_command=True)

        # We need to remove the "uptime" values here.  That will trigger any attempt at comparison as it's
        # always changing
        for route in routing_table:

            del route["uptime"]

        # disconnect from the client
        ssh_client.session.disconnect()

    # check to see if the master routes file has already been created.
    if not Paths.file_exists("pre_migration_route_table.json"):

        with open("pre_migration_route_table.json", "w") as master:
            master.write(json.dumps(routing_table))

    else:

        return routing_table


def compare_routing_tables(ip_address: str, credential_id: str, platform: str):
    """
    compare_routing_tables summary
        Uses the source of truth file created from the "get_routing_table" function and compares
        that to the current routing table to detect any missing routes from the current routing
        table and those stored in the source of truth file.

    Args:
        ip_address (str): The IP address of the core switch/router to be logged into.  This can
        also be a hostname but note that the hostname should be resolvable to an IP address.

        credential_id (str): This is the prefix used to identify the login credential set in the
        user provided .env file.  Assuming, for example your username was test_username, the 
        credential ID would be "test".  This assumes that all credentials follow this patter.
        Example: test_username, test_password, test_secret, etc.

        platform (str): The Netmiko platform identifier.  Can be "cisco_ios" for IOS based
        devices, "cisco_nexus" for Nexus devices, etc.
    """

    networks = []
    missing_routes = []

    # If the master/reference file has not been created, no need to proceed as we have to have a SOT
    if not Paths.file_exists("pre_migration_route_table.json"):

        return f"Missing the Pre-Migration Route Table"

    else:

        # Get the current routing table to be compared against the reference
        post_migration_routes = get_routing_table(ip_address = ip_address, credential_id = credential_id, platform = platform)

        # open the pre-migration route table for comparison
        with open("pre_migration_route_table.json", "r") as reference_routes:

            pre_migration_route_table = json.load(reference_routes)

            # loop through the pre-migration routes and pull out the network
            for reference in pre_migration_route_table:
                route = reference["network"]

                # loop through the post-migration routes and pull out the network and add it to a list
                for comparison in post_migration_routes:
                    networks.append(comparison["network"])

                # probably not the most efficient way to do this, but its stupid simple.
                # take the pre-migration network and see if it is in the list of networks from the 
                # post-migration networks.  if it isn't, append the entire pre-migration route to the 
                # missing routes list
                if route not in networks:
                    missing_routes.append(reference)
                else:
                    # if the pre-migration network is in the list, the clear the list and continue
                    networks = []
                    continue
        
        # if the missing routes list is empty, it means there are no missing routes
        if len(missing_routes) == 0:

            # return something to the user even if there are no differences
            missing_routes.append({"Routes Missing":0})
            missing_routes = json.dumps(missing_routes)
            return missing_routes

        else:
            # otherwise convert the missing routes to JSON and write to file
            with open("missing_routes.json", "w") as f:
                f.write(json.dumps(missing_routes))


# let's test this thing out
print(compare_routing_tables(ip_address="192.168.217.2", credential_id="nxos", platform="cisco_nxos"))
# get_routing_table(ip_address="192.168.217.2", credential_id="nxos", platform="cisco_nxos")
