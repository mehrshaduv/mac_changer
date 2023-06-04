#!/usr/bin/env python

from subprocess import check_output, call
from optparse import OptionParser
import re
from colorama import Fore

def get_input():
    parser = OptionParser()
    parser.add_option('-i','--interface', dest='interface', help='Enter your interface use -i or --interface.')
    parser.add_option('-m','--mac', dest='new_mac', help='Enter your favorite mac use -m or --mac.')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error(Fore.RED + "[-] please spesify an interface, --help for more info.")
    elif not options.new_mac:
        parser.error(Fore.RED + "[-] please spesify a MAC address, --help for more info.")
    return options

def changing_mac(interface, new_mac):
    print(Fore.YELLOW + "[*] changing MAC address to " + new_mac)
    call(['ifconfig', interface, 'down'])
    call(['ifconfig', interface,'hw', 'ether', new_mac])
    call(['ifconfig', interface, 'up'])

def check_changing(interface):
    result = check_output(['ifconfig', interface])
    current_mac = re.search('\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', result.decode())
    if current_mac:
        return current_mac.group(0)
    else:
        print(Fore.RED + '[-] Could not to be read MAC address.')

options = get_input()
print(Fore.MAGENTA + "current MAC : " + check_changing(options.interface))
changing_mac(options.interface, options.new_mac)
result = check_changing(options.interface)
if result == options.new_mac:
    print(Fore.GREEN + '[+] MAC address was successful chaned to ' + result)
else:
    print(Fore.RED + '[-] MAC address did not get change.')
