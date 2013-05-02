#!/usr/bin/env python

"""
WhoTrack.py originally written by Keith Gilbert - @digital4rensics
www.digital4rensics.com - 5/1/13 - Version 0.1

The script will track basic domain WhoIs information based upon domains entered in the database.
This is an ongoing work and is likely not suitable for production use at the moment.
Planned improvements for: 1.) Proxy support 2.) Reporting 3.) History Tracking

No warranty is implied or expressed, use at your own risk.

usage: WhoTrack.py [-h] [-d DATABASE] [-i INSERT] [-p PROXIES] [-t TEST]
                   [-s SERVERS] [-v]

Track Daily Domain Registrant Changes

optional arguments:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        Specify database name
  -i INSERT, --insert INSERT
                        Insert new domain in to the database
  -p PROXIES, --proxies PROXIES
                        Specify a list of proxies to conduct lookups
  -t TEST, --test TEST  Bypass database to test parsers against a specific
                        domain
  -s SERVERS, --servers SERVERS
                        Specify different servers file
  -v, --verbose         Enable command line output
"""

import re
import sys
import socks
import socket
import sqlite3
import argparse
from random import choice
from datetime import date

sys.path.append('./')
sys.path.append('./parsers/')

#Import the list of WhoIs servers from file
def genservers(listname):
	try:
		list = open(listname, 'r')
	except:
		ish = "Error opening servers file. Please verify it is located in the same directory and that it exists."
		if verb:
			print ish
	
	#Ignore comments at the beginning of the file
	ignore = re.compile("^;")
	paired = {}
	
	#For each entry, create a key,value pair in the dictionary
	for line in list:
		if not ignore.match(line):
			temp = line.split()
			paired[temp[0]] = temp[1]

	list.close()
	if verb:
		print "Server list successfully generated\n"
	return paired
	
def genproxies(listname):
	try:
		list = open(listname, 'r')
	except:
		ish = "Error opening proxies file. Please verify it is located in the same directory and that it exists."
		if verb:
			print ish

	prox = []
	
	#For each entry, create a key,value pair in the dictionary
	for line in list:
		if line.startswith(";"):
			pass
		else:
			temp = line.rstrip().split(":")
			prox.append(temp)

	list.close()
	if verb:
		print "Proxy list successfully generated\n"
	return prox

#Set up the Database
def dbsetup(name):
	try:
		conn = sqlite3.connect(name, isolation_level=None)
		cur = conn.cursor()
	except:
		ish = "Error connectiong to database\n"
		if verb:
			print ish
		
	try:
		cur.execute("CREATE TABLE IF NOT EXISTS Domains(Domain TEXT, Name TEXT, Org TEXT, Addr TEXT, Email TEXT, Phone TEXT, Fax TEXT)")
		return cur
	except:
		ish = "Error creating database table"
		if verb:
			print ish

def newdomain(dom, db):
	try:
		test = db.execute("SELECT count(*) FROM Domains WHERE Domain = ?", (dom,)).fetchone()[0]
		if test == 0:
			db.execute("INSERT INTO Domains VALUES(?, ?, ?, ?, ?, ?, ?)", (dom,None,None,None,None,None,None))
		else:
			ish = "Domain: " + dom + " already in database, not inserted."
			if verb:
				print ish
	except:
		ish = "Error inserting new domain in to database"
		if verb:
			print ish

#Get Domains to Monitor from Database
def getdata(db):
	try:
		domlist = []
		for row in db.execute("SELECT Domain FROM Domains"):
			domlist.append(row[0])
		return domlist
	except:
		ish = "Error retrieving domains to monitor from database"
		if verb:
			print ish

#Check and Insert Records in Database
def insertdata(data, db, dom):
	test = []
	current = []
	for row in db.execute("SELECT * FROM Domains WHERE Domain = ?", (dom,)):
		for elem in row:
			current.append(elem)
	test.extend([dom, data['name'], data['organization'], data['address'], data['email'], data['phone'], data['fax']])
	i=0
	change = False
	for elem in current:
		#Is the old record the same as the new record?
		try:
			if test[i] == elem:
				i += 1
			else:
				change = True
		except:
			ish = "Error comparing new and old data for: " + data['name']
			if verb:
				print ish
					
	if change:	
		ish = "Change detected\n" + "Old Data: " + str(current) + "\n" + "New Data: " + str(test) + "\n"
		db.execute("UPDATE Domains SET Name=?, Org=?, Addr=?, Email=?, Phone=?, Fax=? WHERE Domain=?", 
		(data['name'], data['organization'], data['address'], data['email'], data['phone'], data['fax'], dom))
		report.write(ish)
		if verb:
			print ish
	else:
		if verb:
			print "No change detected for " + dom
				
#Do the Whois Lookup
def dowhois(dom, col, recurse):
	#Variable to track if the call is recursive
	redo = False
	response = ""
	
	#Find the correct whois server
	if recurse:
		tld, srv = findserver(recurse, col)
		redo = True
	else:	
		tld, srv = findserver(dom, col)
	
	try:
	#Build connection
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((srv, 43))
		if verb:
			print "Connected Successfully to " + srv + " for " + dom
		s.send(dom + "\r\n")

		while True:
			d = s.recv(4096)
			response += d
			if not d:
				break
		s.close()
		record = extractdata(dom, tld, response, redo)
		if record:
			return record
	except:
		ish = "Error in connection to " + srv + " for " + dom
		if verb:
			print ish
		
#Get Correct server to use
def findserver(tld, col):
	try:
		for key in col.keys():
			use = key + "$"
			if re.search(use, tld):
				return key,col[key]
	except:
		ish = "Error finding correct whois server"
		if verb:
			print ish

#Extract the appropriate data from the record
def extractdata(dom, tld, data, stop):
	#If .com and not 2nd query, extract appropriate nameserver and initiate new query
	if tld == "com" or tld == "net" and stop == False:
		reg = re.search('(?<=Registrar: )\w+', data)
		newsrv = reg.group().lower()
		newdata = dowhois(dom, servlist, newsrv)
		return newdata
	#Parse whois results for appropriate data using appropriate plugin
	else:
		#Import the correct parsing module based on TLD or Registrar
		try:
			parse = __import__(tld)
			stripped = parse.parse(data)
			return stripped
		except:
			ish = "Error importing parser"
			if verb:
				print ish

def main():
	global servlist
	global proxylist
	global verb
	global report
	
	parser = argparse.ArgumentParser(description="Track Daily Domain Registrant Changes")
	parser.add_argument("-d", "--database", help="Specify database name")
	parser.add_argument("-i", "--insert", help="Insert new domain in to the database")
	parser.add_argument("-p", "--proxies", help="Specify a list of proxies to conduct lookups")
	parser.add_argument("-r", "--report", help="Specify a report filename other than the default")
	parser.add_argument("-s", "--servers", help="Specify different servers file")
	parser.add_argument("-t", "--test", help="Bypass database to test parsers against a specific domain")
	parser.add_argument("-v", "--verbose", action="store_true", help="Enable command line output")
	args = parser.parse_args()

	#If verbosity is enabled
	if args.verbose:
		verb = True
	else:
		verb = False
		
	#If a custom server file was specified
	if args.servers:
		servlist = genservers(args.servers)
	else:
		servlist = genservers('servers.txt')

	#If testing new parsers
	if args.test:
		testdat = dowhois(args.test, servlist, None)
		print testdat
		
	#If a custom database was specified
	if args.database:
		db = dbsetup(args.database)
	else:
		db = dbsetup('WhoTrack.db')
	
	#If only inserting new domain
	if args.insert:
		newdomain(args.insert, db)
		db.close()
		sys.exit()

	if args.report:
		report = open(args.report, 'w')	
	else:
		rname = date.isoformat(date.today()) + "_Report.txt"
		report = open(rname, 'w')
		
	doms = getdata(db)

	#If you want to use proxies to make the requests
	if args.proxies:
		plist = genproxies(args.proxies)
		for row in doms:
			selection = choice(plist)
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, selection[0], int(selection[1]))
			socket.socket = socks.socksocket
			
			ws = dowhois(row.strip(),servlist, None)
			insertdata(ws, db, row)
	else:
		for row in doms:
			ws = dowhois(row.strip(),servlist, None)
			insertdata(ws, db, row)
	
	db.close()	
	report.close()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit()