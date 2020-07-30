'''
Author: Jake Wachs
Crimson Defense - 2019
'''

'''
TODO:
- Instead of manually checking cmd line, parse for options
- Add suppress output option -s to get rid of excessive printing
- Create port scanner that takes output from this program
- Eventually build a set of chaining programs that become a simple nmap
'''

import sys
import os
import subprocess
import netifaces
from termcolor import colored

def trimIP(ip):
	'''
	Trims IP address to last decimal for concat

	Keyword Arguments:
	ip - IP address to trim as a string

	return - trimmed IP
	'''
	trimmed = ''
	
	numPeriods = 0
	s = len(ip)
	for i in range(0, s):
		if numPeriods == 3:
			break
		
		if ip[i] == '.':
			numPeriods = numPeriods + 1

		trimmed = trimmed + ip[i]

	return trimmed


def scan(r, ip):
	'''
	Function that actually scans the network

	Keyword Arguments:
	r - Max number in the range of IPs
	upHosts - List of active hosts
	noResponse - List of hosts that didn't respond
	failedPing - List of hosts where ping failed
	'''
	r = int(r)

	upHosts = []
	noResponse = []
	failedPing = []

	for i in range(0, r):
		addr = trimIP(ip) + str(i)

		DNULL = open(os.devnull, 'w')
		output = subprocess.call(['ping', '-c', '2', addr], stdout=DNULL, stderr=subprocess.STDOUT)
		if output == 0:
			text = colored(addr + ' host is UP!', 'green')
			print(text)
			upHosts.append(addr)

		elif output == 2:
			text = colored('No response from ' + addr, 'yellow')
			print(text)
			noResponse.append(addr) 

		else:
			text = colored('Ping to ' +  addr + ' failed' )
			failedPing.append(addr)
			print(text)

	return [upHosts, noResponse, failedPing]


if __name__ == '__main__':
	writeToFile = False

	if len(sys.argv) > 1:
		if sys.argv[1] == '-h':
			print('Usage: python3 pingScanner.py <optional_filename>')
			exit()	
		else:
			writeToFile = True

	interfaces = netifaces.interfaces()
	s = len(interfaces)
	
	print('Which interface would you like to scan? Interface options are:')
	for i in range (0, s):
		coloredOption = colored('[' + str(i) + '] ' + str(interfaces[i]), 'yellow')
		print(coloredOption)

	choice = input('Selected interface: ')
	print('Scanning ' + interfaces[int(choice)] + '...')

	ip = netifaces.ifaddresses(interfaces[int(choice)])[netifaces.AF_INET][0]['addr']
	'''
	allDown = None
	upText = None
	downText = None
	'''

	[upHosts, noResponse, failedPing] = scan(24, ip) # FIXME: change this number to 255
	
	# write to file with the date and time

	if writeToFile == True:
		filename = sys.argv[1]
		fp = open(filename, 'w')
		formattedStr = 'upHosts:\n' + str(upHosts) + '\n\nnoResponse:\n' + \
				  str(noResponse) + '\n\nfailedPing:\n' + str(failedPing) + '\n'
		fp.write(formattedStr)
		print('Intelligence logged to ' + filename)
		fp.close()
	else:
		print('upHosts: ', upHosts)
		print('noResponse: ', noResponse)
		print('failedPing: ', failedPing)
'''
while True:
	sh = input('ghostScan>>')
	
	if sh == 'quit' or sh == 'q':
		break

	elif sh == '--help' or sh == '-h' or sh == 'help':
		print('Options: scan, up/uphosts, down/downhosts, file, q/quit')

	elif sh == 'scan' or sh == 's':
		rn = input('What is the max number of the last digit in the IP (0-255):')
		scan(rn)

	elif sh == 'up' or sh == 'uphosts':
		print(upText)

	elif sh == 'down' or sh == 'downhosts':
		print(downText)

	elif sh == 'file':
		filename = input('Enter filename to write:')
		fp = open(filename, 'w')

		fp.write('Up hosts:')
		fp.write(str(upHosts) + '\n\n')

		fp.write('Hosts that did not respond:')
		fp.write(str(noResponse) + '\n\n')

		fp.write('Failed pings to:')
		fp.write(str(failedPing))

		fp.close()
'''	

