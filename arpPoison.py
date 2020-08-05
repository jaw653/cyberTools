'''
Author: Jake Wachs
Aug 2020
'''

'''
This script assumes the attacking device is
already on the network of the victim gateway and endpoint
'''
import re
import os
import sys
import subprocess
from subprocess import Popen, PIPE


def extractIP(line):
	'''
	Gets the IP address from a line of text

	Keyword Arguments:
	line - line of text provided via readline() method

	return - IP address
	'''
	# regex for ip address: /d{1,3}\./d{1,3}\./d{1,3}\./d{1,3}
	ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)

	if len(ip) < 1:
		raise Exception('No default IP address could be found')

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
			try:
				return extractIP(currLine)
			except:
				raise Exception('No default IP address could be extracted')

		currLine = output.stdout.readline().decode('utf-8')


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage: python3 arpPoison.py <target_IP_address>')
		exit(-1)
	else:
		victim_ip = sys.argv[1]

		p = Popen(['ip', 'r'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		try:
			gateway_ip = getDefaultGateway(p)
		except:
			print('No default gateway could be found')		# FIXME: print to stderr
			exit()

		print('gateway ip is: ', gateway_ip)
