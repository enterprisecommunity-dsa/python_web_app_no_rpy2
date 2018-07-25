from flask import session
def lm_output_printer():
	'''
	This takes arguments from the current Flask session object and runs a subprocess command of the form
		"Rscript regression_app/<file type>_reader.R <Uploaded Data Absolute path> <Uploaded Data Filename w/out extension>"
	'''

	cmd = 'Rscript regression_app'
	
	filename = str(session['current_data_abs_path'])
	fe = str(session['current_file_extension'])
	fn = session['current_file_name_no_extension']
	if fe == 'csv':
		cmd += '/csv_reader.R '
	elif fe == 'json':
		cmd += '/json_reader.R '
	else:
		return "{} file type is not supported. Please upload something else.".format(fe)
	
	cmd += filename + ' ' + fn
	import subprocess
	try:
		s = subprocess.run(cmd, check = True, stdout=subprocess.PIPE, encoding='utf-8')
	except subprocess.CalledProcessError:
		return 1
	else:
		return s.stdout

	

# def parser(csv_text_string):
    # '''
    # Takes a csv-formatted text string and formats it into a dictionary ready
    # for JSON parsing
    
    # '''
    # dd = {}
    # lst_of_lines = csv_text_string.split('\n')
    # for i in lst_of_lines:
        # lst_of_elts = i.split(',')
        # dd[lst_of_elts.pop(0)] = lst_of_elts
    # for (k,v) in dd.items():
        # float_lst = []
        # for i in v:
            # float_lst.append(float(i))
        # dd[k] = float_lst
    # return dd

	
def csv_to_json(s):
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
            dd[nums_to_headers_dict[k]].append(line_objs[k])
    return dd
        


def dict_to_command_line_string(dd):
    s = ''
    for (k,v) in dd.items():
        s = s+ ' ' + k
        for i in v:
            s = s + ' ' + i
    return s
