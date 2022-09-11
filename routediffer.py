
import csv
import json
from paths import Paths
from netmiko import ConnLogOnly
from dotenv import load_dotenv

load_dotenv()

# NOTE:
# - TextFSM is not looking at or parsing lines in the table such as: 10.20.22.195/32, ubest/mbest: 1/0
#   - Its only grabbing the actual route(s) that follow those lines
# - The route prefix should be unique and could be a candidate for a key

nxos_headers: list = ["vrf", "protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip", "nexthop_if", "uptime", "nexthop_vrf", "tag", "segid", "tunnelid", "encap"]
ios_headers: list = ["protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip", "nexthop_if", "uptime"]


nexus = {
    "device_type": "cisco_nxos",
    "host": "192.168.217.2",
    "username": "admin",
    "password": "admin"
}

def get_routing_table(profile):

    with ConnLogOnly(**profile) as connection:

        routing_table = connection.send_command("show ip route", use_textfsm=True, strip_prompt=True, strip_command=True)
        connection.disconnect()
        return routing_table

def create_master_route_table(routes, headers):

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
    routing_table = get_routing_table(profile=nexus)
    create_master_route_table(routes=routing_table, headers=nxos_headers)
else:
    pass
    