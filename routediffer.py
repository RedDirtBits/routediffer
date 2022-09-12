
import json
from paths import Paths
from jdiff import extract_data_from_json, CheckType

# nxos_headers: list = ["vrf", "protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip",
# "nexthop_if", "uptime", "nexthop_vrf", "tag", "segid", "tunnelid", "encap"]

# ios_headers: list = ["protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip",
# "nexthop_if", "uptime"]


def get_routing_table(ip_address: str, credential_id: str, platform: str):

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

        return


def compare_routing_tables(ip_address: str, credential_id: str, platform: str):

    # If the master/reference file has not been created, no need to proceed as we have to have a SOT
    if not Paths.file_exists("pre_migration_route_table.json"):

        return f"Missing the Pre-Migration Route Table"

    else:

        # Get the current routing table to be compared against the reference
        migrated_routes = get_routing_table(ip_address = ip_address, credential_id = credential_id, platform = platform)

        # open the pre-migration route table for comparison
        with open("pre_migration_route_table.json", "r") as reference_routes:

            pre_migration_route_table = json.load(reference_routes)

            # initialize jdiff
            comparison = CheckType.create(check_type="exact_match")

            # evaluate the reference against the new/post-migration routing table and flag the differences. if the tables
            # are the same a tuple ({}, True) will be returned, otherwise the differences will.
            differences = comparison.evaluate(pre_migration_route_table, migrated_routes)

            # for now.  probably need to write this to file just for sanity's sake or perhapd return and write to file
            return differences

# let's test this thing out
# print(compare_routing_tables(ip_address="192.168.217.2", credential_id="nxos", platform="cisco_nxos"))
get_routing_table(ip_address="192.168.217.2", credential_id="nxos", platform="cisco_nxos")
