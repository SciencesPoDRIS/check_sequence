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
path_separator = '/'
log_folder = 'log'
log_level = logging.DEBUG

#
# Programm
#
def check(path) :
	logging.info('Check path : ' + path)
	ranks = {}
	lasts = {}
	# Iterate over each folder and file from path
	for file in os.listdir(path) :
		complete_path = os.path.join(path, file)
		# If it is a file
		if os.path.isfile(complete_path) :
			splitted_file = complete_path.split('/')[-1].split('_')
			if len(splitted_file) >= 4 :
				rank = int(splitted_file[4])
				extension = splitted_file[-1].split('.')[-1]
				if not extension in ranks.keys() :
					ranks[extension] = []
				if not extension in lasts.keys() :
					lasts[extension] = -1
				ranks[extension].append(rank)
				lasts[extension] = rank
		# If it's a folder, let's iterate
		else :
			check(complete_path)
	for item in ranks.keys() :
		if lasts[item] != -1 :
			result = compare(ranks[item], lasts[item])
			if len(result) == 0 :
				print 'All the files are present'
			else :
				print 'Files are missing'

def compare(array_01, last_item) :
	array_02 = range(1, last_item + 1)
	return [aa for aa in array_01 if aa not in array_02]

#
# Main
#
if __name__ == '__main__':
	# Check that the command line has at least 2 arguments
	if len(sys.argv) < 2 :
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