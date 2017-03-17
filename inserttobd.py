#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing module for encoding/decoding
import codecs
# Importing module for work with SQLite database
import sqlite3
# Importing module for work with operating system
import os 
# if_debug
import time
class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()
         
    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)
# end if_debug

# Funtion for searching of entrance of a line in the list
def search(t, f):
	numb = 0
	for i in t:
		if (f == i[0]):
			return numb
		numb += 1
	
	return False
'''	
alphabet = [u'\u0410', u'\u0411', u'\u0412', u'\u0413', u'\u0414', u'\u0415', u'\u0416', u'\u0417', u'\u0418', u'\u0419', u'\u041A', 
 u'\u041B', u'\u041C', u'\u041D', u'\u041E', u'\u041F', u'\u0420', u'\u0421', u'\u0422', u'\u0423', u'\u0424', u'\u0425', u'\u0426', 
 u'\u0427', u'\u0428', u'\u0429', u'\u042A', u'\u042B', u'\u042C', u'\u042D', u'\u042E', u'\u042F', u'\u0430', u'\u0431', u'\u0432', 
 u'\u0433', u'\u0434', u'\u0435', u'\u0436', u'\u0437', u'\u0438', u'\u0439', u'\u043A', u'\u043B', u'\u043C', u'\u043D', u'\u043E', 
 u'\u043F', u'\u0440', u'\u0441', u'\u0442', u'\u0443', u'\u0444', u'\u0445', u'\u0446', u'\u0447', u'\u0448', u'\u0449', u'\u044A', 
 u'\u044B', u'\u044C', u'\u044D', u'\u044E', u'\u044F' ]
'''
punc_mark = ['.', ',', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '"', '-', ':', 'N', '(', ')', '[', ']', 
';', '—', 'X', 'I', 'V', '\r', '\n', ' ', '\'']
new_line = ''
percent = 0
# Getting and printing files in directory Text1
files = os.listdir('./Text1')
files.sort()
print 'Files:'
for file in files:
	print file

# Opening connection with database
conn = sqlite3.connect('atribution_text')
cur = conn.cursor()

# Reading line from input file and concating its in one line
for file in files:
	ind = file.find('.')
	cur.execute("SELECT author FROM authors WHERE author='%s'"%file[:ind])
	flag = cur.fetchone()
	if not(flag):
		cur.execute("INSERT INTO authors(author, text) VALUES ('%s','%s')"%(file[:ind], file[ind + 1:]))
		conn.commit()
		cur.execute('SELECT last_insert_rowid()')
		author_id = cur.fetchone()[0] 
		new_line = ''
		with open('./Text1/' + file, 'r') as f:
			for line in f.readlines():
				for let in line:
					if not(let in punc_mark):
						new_line += let
					elif let != '\n':
						if new_line[len(new_line) - 1:len(new_line) - 0] != ' ':
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
			cur.execute("SELECT id FROM triads WHERE triad='%s'"%triad[0])
			triad_id = cur.fetchone()
			if (triad_id):
				triad_id = triad_id[0]
			else:	
				cur.execute("INSERT INTO triads(triad) VALUES ('%s')"%triad[0])
				conn.commit()
				cur.execute('SELECT last_insert_rowid()')
				triad_id = cur.fetchone()[0] 
			#print triad_id
			#print author_id
			cur.execute("INSERT INTO author_has_triad(author_id, triad_id, quantity) VALUES ('%i','%i', '%i')"%(author_id, triad_id, 
				triad[1]))
			conn.commit()

	percent += 10
	print 'Complete ' + str(percent) + '%'

# Closing connection with database
cur.close()
conn.close()