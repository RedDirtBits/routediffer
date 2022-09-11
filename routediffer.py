
import csv
import json
from paths import Paths

# NOTE:
# - TextFSM is not looking at or parsing lines in the table such as: 10.20.22.195/32, ubest/mbest: 1/0
#   - Its only grabbing the actual route(s) that follow those lines
# - The route prefix should be unique and could be a candidate for a key

nxos_headers: list = ["vrf", "protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip", "nexthop_if", "uptime", "nexthop_vrf", "tag", "segid", "tunnelid", "encap"]
ios_headers: list = ["protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip", "nexthop_if", "uptime"]


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

        # disconnect from the client
        ssh_client.session.disconnect()

        return routing_table

def create_master_route_table(routes: json, headers: list = []):

    with open("master_route_table.csv", "w") as master_copy:

        write_routes = csv.DictWriter(master_copy, fieldnames=headers)
        write_routes.writeheader()

        for route in routes:
            write_routes.writerow({
                "vrf": route["vrf"],
                "protocol": route["protocol"],
                "type": route["type"],
                "network": route["network"],
                "mask": route["mask"],
                "distance": route["distance"],
                "metric": route["metric"],
                "nexthop_ip": route["nexthop_ip"],
                "nexthop_if": route["nexthop_if"],
                "nexthop_vrf": route["nexthop_vrf"],
            })

# if the master routing table does not already exist, it needs to be created
if not Paths.file_exists("master_route_table.csv"):

    try:
        routing_table = get_routing_table(ipaddr="192.168.217.2", credential_id="nxos", platform="cisco_nxos")
    except ValueError as e:
        print(e)
    except ImportError as e:
        print(e)
    else:
        # if there are no errors from getting the routing table, then parse it out into the CSV file
        create_master_route_table(routes=routing_table, headers=nxos_headers)

else:
    pass
    