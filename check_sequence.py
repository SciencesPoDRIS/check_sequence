#!/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python check_sequence.py "path/to/folder/to/check"

#
# Libs
#
import logging
import os
import sys

#
# Config
#
# Linux style
# path_separator = '/'
# Windows style
path_separator = '\\'
log_folder = 'log'
log_level = logging.DEBUG
file_separator = '_'
# Rank number in file pattern, couting starts with 0. Check the file_separator above.
rank_file_pattern = 4

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
			splitted_file = complete_path.split(path_separator)[-1].split(file_separator)
			if len(splitted_file) >= rank_file_pattern :
				try :
					rank = int(splitted_file[rank_file_pattern].split('.')[0])
				except ValueError as e :
					logging.error('Error : could not convert data to an integer. The rank is not correctly setted.')
					print 'Error : could not convert data to an integer. The rank is not correctly setted.'
					sys.exit()
				extension = splitted_file[-1].split('.')[-1]
				if not extension in ranks.keys() :
					ranks[extension] = []
				if not extension in lasts.keys() :
					lasts[extension] = -1
				if not extension in names :
					tmp = rank_file_pattern + 1
					names[extension] = file_separator.join(splitted_file[:tmp]) + file_separator + 'RANK' + file_separator + splitted_file[-1]
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
			logging.info('Everything worked well. Your folder is sooooo perfect !')
			print 'Everything worked well. Your folder is sooooo perfect !'