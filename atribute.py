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

# Function for searching of entrance of a line in the list
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
# Getting and printing files in directory Text2
if __debug__:
	direc = './Test'
else:
	direc = './Text2'
files = os.listdir(direc)
files.sort()
print 'Files:'
i = 0
difference = []
for file in files:
	i += 1
	print str(i) + ' ' + file
num = int(input('Input file number: '))
new_line = ''
with open(direc + '/' + files[num - 1], 'r') as f:
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
# Opening connection with database
if __debug__:
	conn = sqlite3.connect('test')
else:
	conn = sqlite3.connect('atribution_text')
cur = conn.cursor()
# Get authors list from database
cur.execute("SELECT * FROM authors")
authors = cur.fetchall()
for author in authors:
	cur.execute("""SELECT triads.triad, author_has_triad.quantity 
					FROM author_has_triad, triads 
					WHERE author_has_triad.author_id=%s AND author_has_triad.triad_id=triads.id"""%(author[0]))
	distribution = cur.fetchall()
	if __debug__:
		print distribution
	# Comparision
	tmp = 0.0
	count = 0.0
	for triad in distribution:
		ind = search(triads, triad[0])
		if ind != -1:
			tmp += 1.0 * abs(triads[ind][1] - triad[1]) / triad[1]
		else:
			count += triad[1] 
	for triad in triads:
		if (search(distribution, triad[0]) == -1):
			count += triad[1]
	difference.append(1.0 * (count + tmp) / len(distribution)) #list_sum(distribution))

print difference
print authors[difference.index(min(difference))][1] 
if __debug__:
	print "Elapsed time: {:.3f} sec".format(time.time() - tim)
# Closing connection with database
cur.close()
conn.close()