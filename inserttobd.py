#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing module for encoding/decoding
import codecs
# Importing module for work with SQLite database
import sqlite3
# Importing module for work with operating system
import os 
# Importing module for work with time
import time

# Funtion for searching of entrance of a line in the list
def search(t, f):
	numb = 0
	for i in t:
		if (i[0] == f):
			return numb
		numb += 1
	
	return -1

if __debug__:
	tim = time.time()
punc_mark = ['.', ',', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '"', '-', ':', 'N', '(', ')', '[', ']', 
';', '—', 'X', 'I', 'V', '\r', '\n', ' ', '\'', 'a', 'b', 'c', 'd', 'e', 'f', '–', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
new_line = ''
percent = 0
# Getting and printing files in directory Text1
if __debug__:
	direc = './Test'
else:
	direc = './Text1'
files = os.listdir(direc)
files.sort()
print 'Files:'
for file in files:
	print file
# Opening connection with database
if __debug__:
	conn = sqlite3.connect('test')
else:
	conn = sqlite3.connect('atribution_text')
cur = conn.cursor()
count = 0
# Reading line from input file and concating its in one line
for file in files:
	count += 1
	ind = file.find('.')
	if __debug__ and file.find('1') != -1 :
		continue
	cur.execute("SELECT author FROM authors WHERE author='%s'"%file[:ind])
	flag = cur.fetchone()
	if not(flag):
		cur.execute("INSERT INTO authors(author, text) VALUES ('%s','%s')"%(file[:ind], file[ind + 1:]))
		conn.commit()
		author_id = cur.lastrowid
		new_line = ''
		with open(direc + '/' + file, 'r') as f:
			for line in f.readlines():
				for let in line:
					if not(let in punc_mark):
						new_line += let
					elif let != '\n':
						if new_line[len(new_line) - 1:len(new_line)] != ' ':
							new_line += ' '
								
		# Print turned-out line		
		new_line = new_line.decode('utf-8').lower()
		# Splitting text into triads
		i = 0
		triads = []
		while (i < len(new_line) - 2):
			temp = 0
			if (new_line[i + 1] != ' '):
				temp = search(triads, new_line[i:i + 3])
				if (temp != -1):
					triads[temp][1] += 1
				else:
					triads.append([new_line[i:i + 3], 1])
			i += 1
		# Sort list of triads
		triads.sort()
		# Work with database
		for triad in triads:
			cur.execute("SELECT id FROM triads WHERE triad='%s'"%triad[0])
			triad_id = cur.fetchone()
			if (triad_id):
				triad_id = triad_id[0]
				#соббирать одид длинный запрос на кучу вставок, если триада уже есть в базе
				
			else:	
				cur.execute("INSERT INTO triads(triad) VALUES ('%s')"%triad[0])
				conn.commit()
				triad_id = cur.lastrowid
			cur.execute("INSERT INTO author_has_triad(author_id, triad_id, quantity) VALUES ('%i','%i', '%i')"%(author_id, triad_id, triad[1]))
		conn.commit()
	if __debug__:
		print count
		print "Elapsed time: {:.3f} sec".format(time.time() - tim)
	percent += 1
	print 'Complete ' + str(1.0 * percent / len(files) * 100)  + '%'

if __debug__:
	print "Elapsed time: {:.3f} sec".format(time.time() - tim)
# Closing connection with database
cur.close()
conn.close()