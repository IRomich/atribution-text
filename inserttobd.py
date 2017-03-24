#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import module for encoding/decoding
import codecs
# Import module for work with SQLite database
import sqlite3
# Import module for work with operating system
import os 
# Import module for work with time
import time

# Funtion for searching of entrance of a line in the list
def search(t, f):
	numb = 0
	l = len(t)
	while numb < l:
		if t[numb] == f:
			return numb
		numb += 1
	return -1

# Saving current time
start_time = time.time()
# Getting 'alphabet' from file and decoding it from utf 8, splitting by ','
alphabet = open("alphabet", "r").read().decode('utf8', 'ignore').split(',')
# Getting, sorting and printing files in directory Text1
folder = 'Text1'
files = os.listdir(folder)
files.sort()
print 'Files in folder \'' + folder + '\':'
for file in files:
	print file
# Opening connection with database
conn = sqlite3.connect('atribution_text')
cur = conn.cursor()
count = 0
for file in files:
	count += 1
	ind = file.find('.')
	cur.execute("SELECT author FROM authors WHERE author='%s'"%file[:ind])
	if not(cur.fetchone()):
		cur.execute("INSERT INTO authors(author, text) VALUES ('%s','%s')"%(file[:ind], file[ind + 1:]))
		conn.commit()
		# Getting last inserted author id 
		author_id = cur.lastrowid
		new_line = ''
		lines = open(folder + '/' + file, 'r').read().decode('utf8', 'ignore')
		for line in lines:
			for let in line:
				if let in alphabet:
					new_line += let
				elif new_line[len(new_line) - 1:len(new_line)] != ' ':
					new_line += ' '								
		# Translation to lower register	
		new_line = new_line.lower()
		# Splitting text into triads
		i = 0
		triads = []
		while (i < len(new_line) - 2):
			temp = 0
			# If middle element is not space
			if (new_line[i + 1] != ' '):
				# Search current triad in triads list 
				temp = search(triads, new_line[i:i + 3])
				if (temp != -1):
					# Increment count founded triad
					triads[temp][1] += 1
				else:
					# Add new triad
					triads.append([new_line[i:i + 3], 1])
			i += 1
		# Sort triads list
		triads.sort()
		# Work with database
		for triad in triads:
			# Current triad search in database
			cur.execute("SELECT id FROM triads WHERE triad='%s'"%triad[0])
			triad_id = cur.fetchone()
			if (triad_id):
				# If found then getting 0 element of list
				triad_id = triad_id[0]				
			else:
				# If not found then insert triad to data base	
				cur.execute("INSERT INTO triads(triad) VALUES ('%s')"%triad[0])
				conn.commit()
				# Getting id of just inserted triad
				triad_id = cur.lastrowid
			cur.execute("INSERT INTO author_has_triad(author_id, triad_id, quantity) VALUES ('%i','%i', '%i')"%(author_id, triad_id, triad[1]))
		# Execute transaction 
		conn.commit()
	# Output complete percent and spent time 	
	print 'Complete ' + str(1.0 * count / len(files) * 100)  + '%'
	print 'Elapsed time: {:.3f} sec'.format(time.time() - start_time)

# Output spent time for script work
print 'Elapsed time: {:.3f} sec'.format(time.time() - start_time)
# Closing connection with database
cur.close()
conn.close()