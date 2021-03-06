#!/usr/bin/env python
#
# Create a VLAN interface on top of a physical interface
# given parameters in code as global vars
# and VLAN / prefix / interface names as arguments
#
# rschmied@cisco.com
#
import argparse
import netaddr
import re
import requests
import sys

sys.path.append('../../module03/03-environment-03-mission/')
import hello_lab
import myspark


HOST = 'devnetapi.cisco.com/sandbox/restconf'
PORT = 9443
USER = 'root'
PASS = 'C!sc0123'
BASE = 'GigabitEthernet2'


def create_vlan(host, port, user, password, interface, vlan, ip, insecure):
	"""Function to create a subinterface on CSR1000V."""
	intfc = re.compile(r'^(\D+)(\d+)$')
	m = intfc.match(interface)
	if m is None:
		print("invalid interface name. Valid example: ", BASE)
		return -1

	data = '''
	{
	  "ned:%s": {
	    "name": "%s.%d",
	    "encapsulation": {
	      "dot1Q": {
		    "vlan-id": %d
	      }
	    },
	    %s
	  }
	}
	'''

	if ip.version == 6:
		ipdata = '''
		    "ipv6": {
		      "address": {
			    "prefix-list": [
			      {
			        "prefix": "%s"
			      }
			    ]
		      }
		    }
		''' % str(ip)
	else:
		ipdata = '''
		    "ip": {
		      "address": {
			    "primary": {
			      "address": "%s",
			      "mask": "%s"
			    }
		      }
		    }
		''' % (ip.ip, ip.netmask)

	data      = data % (m.group(1), m.group(2), vlan, vlan, ipdata)
	url       = "https://%s/api/running/native/interface/%s/%s.%d" % (host, m.group(1), m.group(2), vlan)
	headers   = {'content-type': 'application/vnd.yang.data+json', 'accept': 'application/vnd.yang.data+json'}

	try:
		result = requests.put(url, auth=(user, password), data=data, headers=headers, verify=not insecure)
		room = myspark.spark_get_room_id(hello_lab.TOKEN, hello_lab.NAME)
		myspark.spark_send_message(hello_lab.TOKEN, room, "Hi! I'm adding a configuration change now to the CSR1000V!")
		myspark.spark_send_message(hello_lab.TOKEN, room, "Here is the change being applied using RESTCONF:")
		myspark.spark_send_message(hello_lab.TOKEN, room, "URL: %s" % url)
		myspark.spark_send_message(hello_lab.TOKEN, room, "JSON: %s" % data)


	except:
		print(str(sys.exc_info()[0]))
		return -1

	# we expect a 201 for success
	if result.status_code == 201:
		return 0

	# something went wrong
	print(result.status_code, result.text)
	return -1


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('vlan', help = "VLAN number (1-4094)", type=int)
	parser.add_argument('prefix', help = "IPv4 or IPv6 prefix")
	parser.add_argument('--insecure', '-k', action='store_true', help = "relax SSL verification")
	parser.add_argument('--interface', '-i', default=BASE, help = "interface name to use")
	parser.add_argument('--user', '-u', default=USER, help = "user name on remote host")
	parser.add_argument('--password', '-p', default=PASS, help = "password on remote host")
	parser.add_argument('--port', '-P', default=PORT, help = "port on remote host")
	parser.add_argument('--host', '-H', default=HOST, help = "remote host")
	args = parser.parse_args()

	# check for valid VLAN ID
	if args.vlan < 1 or args.vlan > 4094:
		parser.print_usage()
		print ("invalid VLAN ID %s" % str(args.vlan))
		return -1

	# check for valid prefix
	try:
		ip = netaddr.IPNetwork(args.prefix)
	except netaddr.core.AddrFormatError as e:
		parser.print_usage()
		print(e)
		return -1


	# insecure?
	if args.insecure:
		requests.packages.urllib3.disable_warnings()

	return create_vlan(args.host, args.port, args.user, args.password,args.interface, args.vlan, ip, args.insecure)


if __name__ == '__main__':
	sys.exit(main())
