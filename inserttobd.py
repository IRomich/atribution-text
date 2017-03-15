#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing module for encoding/decoding
import codecs
# Importing module for work with SQLite database
import sqlite3
# Importing module for work with operating system
import os 

# Funtion for searching of entrance of a line in the list
def search(t, f):
	numb = 0
	for i in t:
		if (f == i[0]):
			return numb
		numb += 1
	
	return False
	
punc_mark = ['.', ',', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '"', '-', ':', 'N', '(', ')', '[', ']', ';', '—']
# Reading line from input file and concating its in one line
new_line = ''
# Getting and printing files in directory Text
files = os.listdir('./Text')
for file in files:
	print file

# Opening connection with database
conn = sqlite3.connect('atribution_text')
c = conn.cursor()

for file in files:
	ind = file.find('.')
	c.execute("SELECT author FROM authors WHERE author='%s'"%file[:ind])
	flag = c.fetchone()
	if not(flag):
		c.execute("INSERT INTO authors(author, text) VALUES ('%s','%s')"%(file[:ind], file[ind + 1:]))
		conn.commit()
		c.execute("SELECT id FROM authors WHERE author='%s'"%file[:ind])
		author_id = c.fetchone()
		author_id = author_id[0]
		new_line = ''
		with open('./Text/' + file, 'r') as f:
			for line in f.readlines():
				for let in line:
					if let in punc_mark:
						new_line += ' '
					elif let != '\n':
						new_line += let
					
		# Print turned-out line		
		new_line = new_line.decode('utf-8').lower()
		#print new_line

		# Splitting text into triads
		i = 0
		triads = []
		while (i < len(new_line) - 2):
			temp = 0
			if (new_line[i + 1] != ' '):
				temp = search(triads, new_line[i:i + 3])
				if (temp):
					triads[temp][1] += 1
				else:
					triads.append([new_line[i:i + 3], 1])
			i += 1
		# Sort list of triads
		triads.sort()
		# Work with database
		for triad in triads:
			#print triad[0] + ' count: ' + str(triad[1])
			c.execute("SELECT id FROM triads WHERE triad='%s'"%triad[0])
			triad_id = c.fetchone()
			if (triad_id):
				triad_id = triad_id[0]
			else:	
				c.execute("INSERT INTO triads(triad) VALUES ('%s')"%triad[0])
				conn.commit()
				c.execute("SELECT id FROM triads WHERE triad='%s'"%triad[0])
				triad_id = c.fetchone()
				triad_id = triad_id[0]
			#print triad_id
			#print author_id
			c.execute("INSERT INTO author_has_triad(author_id, triad_id, quantity) VALUES ('%i','%i', '%i')"%(author_id, triad_id, triad[1]))
			conn.commit()

# Closing connection with database
c.close()
conn.close()