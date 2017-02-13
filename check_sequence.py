#!/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python check_sequence.py "path/to/folder/to/check"

#
# Libs
#
import logging, os, sys

#
# Config
#
# Linux style
# path_separator = '/'
# Windows style
path_separator = '\\'
log_folder = 'log'
log_level = logging.DEBUG

#
# Programm
#
def check(path) :
	global flag
	logging.info('Check path : ' + path)
	ranks = {}
	lasts = {}
	names = {}
	# Iterate over each folder and file from path
	for file in os.listdir(path) :
		complete_path = os.path.join(path, file)
		# If it is a file
		if os.path.isfile(complete_path) :
			splitted_file = complete_path.split(path_separator)[-1].split('_')
			if len(splitted_file) >= 4 :
				rank = int(splitted_file[4].split('.')[0])
				extension = splitted_file[-1].split('.')[-1]
				if not extension in ranks.keys() :
					ranks[extension] = []
				if not extension in lasts.keys() :
					lasts[extension] = -1
				if not extension in names :
					names[extension] = '_'.join(splitted_file[:5]) + '_RANK_' + splitted_file[-1]
				ranks[extension].append(rank)
				lasts[extension] = rank
		# If it's a folder, let's iterate
		else :
			check(complete_path)
	for item in ranks.keys() :
		if lasts[item] != -1 :
			results = compare(ranks[item], lasts[item], item)
			if len(results) != 0 :
				flag = 0
				print 'These files are missing :'
				for result in results :
					print names[item].replace('RANK', str(result).zfill(6))

# Check if the elements of sequence are not in array
def compare(array, last_index, item) :
	first_index = 3 if item == 'xml' else 1
	sequence = range(first_index, last_index + 1)
	return [s for s in sequence if s not in array]

#
# Main
#
if __name__ == '__main__':
	flag = 1
	# Check that the command line has exactly 2 arguments
	if len(sys.argv) != 2 :
		print ''
		print 'Arguments error'
		print 'Correct usage : ' + sys.argv[0] + ' "path/to/folder/to/check"'
		print 'The argument is mandatory and is the path to a folder containing the files to check'
	else :
		check_path = sys.argv[1]
		# Check that log folder exists, else create it
		if not os.path.exists(log_folder) :
			os.makedirs(log_folder)
		log_file = log_folder + path_separator + sys.argv[0].replace('.py', '.log')
		logging.basicConfig(filename = log_file, filemode = 'w', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
		logging.info('Start')
		check(check_path)
		if flag :
			print 'Everything worked well. Your folder is sooooo perfect !'