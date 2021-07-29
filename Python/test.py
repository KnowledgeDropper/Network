##This is a script to STIG IOS Switch##

from netmiko import ConnectHandler
from getpass import getpass

device = {
    "host": "/home/jdehner/network-scripts/switches"
}

commands = ["logging buffered 100000"]
with ConnectHandler(**device) as net_connect:
    output = net_connect.send_config_set(commands)

print()
print(output)
print()

commands = ["no ip http server"]
with ConnectHandler(**device) as net_connect:
    output = net_connect.send_config_set(commands)

print()
print(output)
print()

commands = ["service password-encryption"]
with ConnectHandler(**device) as net_connect:
    output = net_connect.send_config_set(commands)
    output += net_connect.save_config()

print()
print(output)
print()
