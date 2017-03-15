#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sqlite3

def search(t, f):
	numb = 0
	for i in t:
		if (f == i[0]):
			return numb
		numb += 1
	
	return False

punc_mark = ['.', ',', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# Read line from input file and concate its in one line
new_line = ''
with open('text.txt', 'r') as f:
	for line in f.readlines():
		
		for let in line:
			if let in punc_mark:
				new_line += ' '
			elif let != '\n':
				new_line += let
				
# Print turned-out line		
new_line = new_line.decode('utf-8').lower()
print new_line

# Splitting text into triads
i = 0
triads = []
while (i < len(new_line) - 2):
	temp = 0
	if (new_line[i+1] != ' '):
		temp = search(triads, new_line[i:i + 3])
		if (temp):
			triads[temp][1] += 1
		else:
			triads.append([new_line[i:i + 3], 1])
	i += 1

# Sort list of triads
triads.sort()

# Work with database
conn = sqlite3.connect('atribution_text')
c = conn.cursor()
for triad in triads:
	print triad[0] + ' count: ' + str(triad[1])
	c.execute("INSERT INTO author(author, text) VALUES ('%s','%s')"%('P', '1'))
	conn.commit()

c.close()
conn.close()