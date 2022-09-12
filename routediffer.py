
import json
from paths import Paths
from jdiff import extract_data_from_json, CheckType

# nxos_headers: list = ["vrf", "protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip", "nexthop_if", "uptime", "nexthop_vrf", "tag", "segid", "tunnelid", "encap"]
# ios_headers: list = ["protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip", "nexthop_if", "uptime"]


def get_routing_table(ipaddr: str = None, credential_id: str = None, platform: str = None):

    # run the import statemements from within the function as it makes it easier to 
    # work with the loggging in
    from client import SSHClient
    from ciscocmds import CiscoCommands

    # lets make sure the required information has been provide and if not
    # try and gracefully handle that
    if ipaddr == None or credential_id == None or platform == None:

        raise ValueError("IP Address, Credential ID and Platorm Type are required")
    
    else:

        # if there were no exceptions, everything needed should be preset therefore proceed with
        # the log in to get the routing table
        ssh_client = SSHClient(hostname=ipaddr, profile=credential_id, platform=platform)
        ssh_client.ssh_host_login()

        routing_table = ssh_client.session.send_command(CiscoCommands.show_routes(), use_textfsm=True, strip_prompt=True, strip_command=True)

        # We need to remove the "uptime" values here.  That will trigger any attempt at comparison as it's always changing
        for route in routing_table:
            del route["uptime"]

        # disconnect from the client
        ssh_client.session.disconnect()

        return routing_table

def create_master_route_table(routes: json = {}):

    if len(routes) == 0:

        raise ValueError("It appears the routing table is missing")
    
    else:

        with open("master_route_table.json", "w") as master:

            master.write(json.dumps(routes))

def compare_routing_tables(reference_routes):

    # If the master/reference file has not been created, no need to proceed
    # as we have to have a SOT
    if not Paths.file_exists("master_route_table.json"):

        return f"Missing the Master Route Table"

    else:

        master_route_table = reference_routes

        # Get the current routing table to be compared against the reference
        migrated_routes = get_routing_table(ipaddr="192.168.217.2", credential_id="nxos", platform="cisco_nxos")

        # initialize jdiff
        comparison = CheckType.create(check_type="exact_match")

        # evaluate the reference against the new/post-migration routing table and flag the differences
        differences = comparison.evaluate(master_route_table, migrated_routes)
        print(differences)

with open("master_route_table.json") as master:

    routes = json.load(master)
    compare_routing_tables(reference_routes=routes)

# some_routes = get_routing_table(ipaddr="192.168.217.2", credential_id="nxos", platform="cisco_nxos")
# create_master_route_table(get_routing_table(ipaddr="192.168.217.2", credential_id="nxos", platform="cisco_nxos"))