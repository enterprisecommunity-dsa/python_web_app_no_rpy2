from flask import session
import os
def lm_output_printer():
	'''
	This takes arguments from the current Flask session object and runs a subprocess command of the form
		"Rscript regression_app/<file type>_reader.R <Uploaded Data Absolute path> <Uploaded Data Filename w/out extension>"
	'''
	
	#cmd = 'bin/Rscript'
	#cmd = cmd + ' ' '~/regression_app/csv_reader_new.R'+ ' '
	cmd = '.root/usr/bin/Rscript /app/regression_app/csv_reader_new.R'
	# filename = str(session['current_data_abs_path'])
	# fe = str(session['current_file_extension'])
	# fn = session['current_file_name_no_extension']
	# if fe == 'csv':
		# cmd += '/csv_reader.R '
	# elif fe == 'json':
		# cmd += '/json_reader.R '
	# else:
		# return "{} file type is not supported. Please upload something else.".format(fe)
	
	# cmd += filename + ' ' + fn
	current_data_txt = session['current_data']
	cmd_line_text = dict_to_command_line_string(csv_to_dict(current_data_txt)) 
	#cmd += session['current_dependent_variable']+ ' '+ cmd_line_text
	
	import subprocess
	try:
		s = subprocess.run(cmd, check = True, stdout=subprocess.PIPE, encoding='utf-8')
	except subprocess.CalledProcessError:
		return 1
	else:
		return s.stdout

	
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
