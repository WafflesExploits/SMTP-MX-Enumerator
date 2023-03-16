#!/usr/bin/env python3
import subprocess
import re
import sys
import argparse
import time
from time import sleep
from datetime import datetime



parser = argparse.ArgumentParser(description='-> Enumerates mail servers from domains using MX/A records.')
parser.add_argument('-d', '--domain', type=str, help='Domains to enumerate.')
parser.add_argument('-sn', '--scannum', type=int, nargs='?', help='Number of times to search for multiple A records from found mail servers.', default=10)
parser.add_argument('-st', '--sleeptime', type=int, nargs='?', help='Time before each search of A records. Useful to prevent timeout and avoid being detected.', default=0)
parser.add_argument('-dm', '--debugmode', action='store_true', help='Shows Errors')
parser.add_argument('-v', '--verbose', action='store_true', help='VerboseMode')

args = parser.parse_args()

Domain = args.domain
ScanNum = args.scannum
SleepTime = args.sleeptime
DebugMode = args.debugmode
verbose = args.verbose
NumberOfArgs = len(sys.argv)
if (NumberOfArgs==1): # If there is no arguments, prints out the Script's Usage.
	parser.print_usage()
	sys.exit()

def RegexFinder(pattern, data): # Matches text from data based on regex pattern.
	return re.finditer(pattern, data)

def cmd(cmdstr):
	try:
		strlist = cmdstr.split() # Splits the command into a list ["host", "-t", "mx",...]
		return (subprocess.check_output(strlist, stderr=subprocess.STDOUT).decode('utf-8')) # Executes the cmd and returns output
	except Exception as error:
		if(DebugMode):
			print(error.output, " ", error)
		return str(error.output)



if __name__=='__main__': # Only runs when executed as a script.
	
	currentDate = str(datetime.now())
	StartTime = time.time()
	print(f"* Starting SMTP Records Enum at {currentDate[:-6]}");
	print("| ")
	print("| Settings:")
	print(f"| Number of Scans: {ScanNum} | Delay time between scans: {SleepTime}")
	print("|")
	print("| Credits:")
	print("| By (https://github.com/WafflesExploit)")
	# Get MX Records and Respective Priority
	data = cmd(f"host -t mx {Domain}") # Uses host to extract MX records from Domain
	
	if("no servers could be reached" in data):
		print("Server timed out. Try again later or check if the domain is alive.")
		sys.exit()

	MS_Matches = RegexFinder('\d+ .{1,20}', data)
	if(verbose):
		print("| Extracting MX Records...")
	try:
		MSPriority = [] # Mail Servers Priority
		for matches in MS_Matches:
			matchstring = RegexFinder('^\d+', matches.group())
			for match in matchstring:
				MSPriority.append(match.group())
	except Exception as error:
		if(DebugMode):
			print(f"Error (code {error}): {error.output}")
		else:
			print("| Something went wrong while extracting the MX Records")
			print("| Run with --debugmode to show error")
	
	if(verbose):
		print("| Extracting Mail Servers Priorities...")
	try:
		MS_Matches = RegexFinder('\d+ .{1,50}', data)
		MailS = [] # Mail Servers Only
		for matches in MS_Matches:
			matchstring = (matches.group())[2:-1] # R
			MailS.append(matchstring.replace(" ", ""))
	except Exception as error:
		if(DebugMode):
			print(f"Error (code {error}): {error.output}")
		else:
			print("| Something went wrong while extracting Mail Servers Priorities")
			print("| Run with --debugmode to show error")
	
	if(verbose):
		print("| Found these Mail Servers")
		index = 0
		for mailserver in MailS:
			index += 1
			print(f"| [{index}] {mailserver}")
	
	# Get A Records(IPv4) from Mail Servers
	if(verbose):
		print("| Extracting A Records (IPv4 addresses)...")
	MailServers = {} # Dictionary that stores A Records with respective Mail Server
	indexy = 1
	for mailservers in MailS:
		addressList = []
		timeout = 0
		for i in range(ScanNum):
			sleep(SleepTime)
			try:
				data = cmd(f"host -t a {mailservers}") # Uses host to extract A records from Domain
				IP_Matches = RegexFinder('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.+', data)
			except Exception as error:
				print("data Error")
				print(error.output, error)
			for matches in IP_Matches:
				strmatch = matches.group()
				if("timed out" in strmatch):
					timeout = timeout + 1
					if(verbose):
						print(f"| {mailservers} Timeout: {timeout}")
				else:	
					addressList.append(matches.group())
				
				sortedAdrsList = list(set(addressList))
				if(timeout>0):
					sortedAdrsList.append(f"timeouts: {timeout}")
		MailServers[indexy]=[mailservers, sortedAdrsList]
		indexy += 1
	index = 1
	for mailservers in MailS:
		if(index not in MailServers.keys()):
			MailServers[index]=[mailservers, "Got Timed Out."]	
		index += 1
	
	
	print("| ")
	print("| Results:")
	EndTime = time.time()
	RunTime = EndTime - StartTime
	print(f"| Domain: {Domain} ")
	print(f"| Finished scan in {str(RunTime)[0:5]}s.")
	MailServers = dict(sorted(MailServers.items()))
	if(len(MailServers) == 0 ):
		print("| No MX Records found.")
	else: 
		for key,value in MailServers.items():
			print(f"| [{key}] MX Record - {value[0]}")
			stringus = ""
			for x in value[1]:
				stringus += x+", "
			print(f"| A Records: {stringus[0:-2]}")
	
	print("*")
