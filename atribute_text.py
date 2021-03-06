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

# Function for search element in list
def search(t, f):
	numb = 0
	for i in t:
		if i[0] == f:
			return numb
		numb += 1
	return -1

# Saving current time
start_time = time.time()
# Getting 'alphabet' from file and decoding it from utf 8, splitting by ','
alphabet = open("alphabet", "r").read().decode('utf8', 'ignore').split(',')
# Getting, sorting and printing files with numbers in directory Text2
folder = './Text2'
files = os.listdir(folder)
files.sort()
print 'Files in folder \'' + folder + '\':'
i = 0
for file in files:
	i += 1
	print str(i) + ' ' + file
num = int(input('Input file number: '))
new_line = ''
lines = open(folder + '/' + files[num - 1], 'r').read().decode('utf8', 'ignore')
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
# Opening connection with database
conn = sqlite3.connect('atribution_text')
cur = conn.cursor()
difference = []
complete = 0
# Getting authors list from database
cur.execute("SELECT * FROM authors")
authors = cur.fetchall()
for author in authors:
	cur.execute("""SELECT triads.triad, author_has_triad.quantity 
					FROM author_has_triad, triads 
					WHERE author_has_triad.author_id=%s AND author_has_triad.triad_id=triads.id"""%(author[0]))
	distribution = cur.fetchall()
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
	difference.append(1.0 * (count + tmp) / len(distribution))
	# Output complete percent and spent time 	
	complete += 1
	print 'Completed ' + str(100.0 * complete / len(authors))  + '%'
	print 'Elapsed time: {:.3f} sec'.format(time.time() - start_time)

print difference
print 'Most likely it is ' + authors[difference.index(min(difference))][1] #+ ' ' + authors[difference.index(min(difference))][2]
# Output spent time for script work
print 'Elapsed time: {:.3f} sec'.format(time.time() - start_time)
# Closing connection with database
cur.close()
conn.close()