'''
Author: Jake Wachs
Crimson Defense - 2019
'''

'''
TODO:
- Create port scanner that takes output from this program
- Eventually build a set of chaining programs that become a simple nmap
'''

import subprocess
import netifaces
from termcolor import colored
interface = input('Enter interface to scan here: ')

netifaces.ifaddresses(interface)		# Using ifconfig to get my box's ip on this interface
ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']

for i in range(0, 255):
	addr = ip[:-1] + str(i)
	output = subprocess.call(['ping', '-c', '3', addr])
	if output == 0:
		text = colored(addr + ' host is UP!', 'green')
		print(text)
	elif output == 2:
		text = colored(addr + 'No response from ' + addr, 'yellow')
		print(text) 
	else:
		text = colored('Ping to ' +  addr + ' FAILED', 'red')
		# print(text)
