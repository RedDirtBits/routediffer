import csv
import json
from netmiko import ConnLogOnly
from dotenv import load_dotenv

load_dotenv()

# NOTE:
# - TextFSM is not looking at or parsing lines in the table such as: 10.20.22.195/32, ubest/mbest: 1/0
#   - Its only grabbing the actual route(s) that follow those lines
# - Need to get the arp table from SJMC Nexus 7k for testing and to update BigMACMaps to work with that

nxos_headers: list = ["vrf", "protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip", "nexthop_if", "uptime", "nexthop_vrf", "tag", "segid", "tunnelid", "encap"]
ios_headers: list = ["protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip", "nexthop_if", "uptime"]


nexus = {
    "device_type": "cisco_nxos",
    "host": "192.168.217.2",
    "username": "admin",
    "password": "admin"
}

with ConnLogOnly(**nexus) as connection:
    result = connection.send_command("show ip route", use_textfsm=True, strip_prompt=True, strip_command=True)
    connection.disconnect()

# with open("original_route_table.csv", "w") as f:
#     file_writer = csv.DictWriter(f, fieldnames=nxos_headers)
#     file_writer.writeheader()

#     for route in result:
#         file_writer.writerow({
#             "vrf": route["vrf"],
#             "protocol": route["protocol"],
#             "type": route["type"],
#             "network": route["network"],
#             "mask": route["mask"],
#             "distance": route["distance"],
#             "metric": route["metric"],
#             "nexthop_ip": route["nexthop_ip"],
#             "nexthop_if": route["nexthop_if"],
#             "nexthop_vrf": route["nexthop_vrf"],
#         })

# print(json.dumps(result))
print(result)