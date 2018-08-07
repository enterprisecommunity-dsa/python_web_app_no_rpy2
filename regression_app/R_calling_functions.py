from flask import session
import os
def lm_output_printer():
	'''
	This takes arguments from the current Flask session object and runs a subprocess command of the form
		"Rscript regression_app/<file type>_reader.R <Uploaded Data Absolute path> <Uploaded Data Filename w/out extension>"
	'''
	
	cmd = 'Rscript regression_app/csv_reader_new.R '

	current_data_txt = session['current_data']
	cmd_line_text = dict_to_command_line_string(csv_to_dict(current_data_txt)) 
	cmd += session['current_dependent_variable']+ ' '+ cmd_line_text
	
	import subprocess
	try:
		s = subprocess.run(cmd, check = True, stdout=subprocess.PIPE, shell = True, encoding='utf-8')
	except subprocess.CalledProcessError:
		return 1
	else:
		return s.stdout




def lm_output_printer_rpy2():
	'''
	This takes arguments from the current Flask session object and runs a subprocess command of the form
		"Rscript regression_app/<file type>_reader.R <Uploaded Data Absolute path> <Uploaded Data Filename w/out extension>"
	'''
	import rpy2.robjects.packages as rpackages
	from rpy2.robjects import (StrVector,
								FloatVector,
								DataFrame, 
								IntVector,
								Formula)
	
	base = rpackages.importr('base')
	utils = rpackages.importr('utils')
	stats = rpackages.importr('stats')
	
	current_df = utils.read_csv(session['current_data_filename'])
	lin_model_object = stats.lm(current_df)
	
	####
	#### Code is stopping here: AttributeError: 'ListVector' object has no attribute 'split'
	####
	
	return(base.summary(lin_model_object))
	


		
		

	












#################################################################################
#####################    UNUSED CODE GOES BELOW    ##############################
#################################################################################


		
def csv_to_dict(s):
	'''
	Takes csv-formatted string and returns a dictionary object which is formatted as one would expect a JSON 
		object to be formatted:
		{"Variable_A":[A_1, A_2, A_3 ..., A_n], "Variable_B":[B_1, ..., B_n],...}
	'''
	list_of_lines = s.split('\n')
	dd = {}
	nums_to_headers_dict = {}
	headers = list_of_lines[0].split(',')
	for i in range(len(headers)):
		nums_to_headers_dict[i] = headers[i].strip()
		dd[nums_to_headers_dict[i]] = []
	for j in list_of_lines[1:]:
		line_objs = j.split(',')
		for k in range(len(line_objs)):
			dd[nums_to_headers_dict[k]].append(line_objs[k].strip())
	return dd
        


def dict_to_command_line_string(dd):
	'''
	A helper function to take the dictionary returned by csv_to_dict and parse it into a string:
		"Variable_A A_1 A_2 ... A_n Variable_B B_1 B_2 ... B_n	
	'''
	s = ''
	for (k,v) in dd.items():
		s = s+ ' ' + k
		for i in v:
			s = s + ' ' + i
	return s
