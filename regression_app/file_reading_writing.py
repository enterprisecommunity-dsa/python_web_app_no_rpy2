from flask import session
def lm_output_printer(filename):
	'''
	Given a filename or relative file path, this function makes an explicit R
	call and returns the printed summary of a linear model
	'''

	cmd = 'Rscript regression_app'
	fe = str(session['file_extension'])
	fn = session['file_name_identifier']
	if fe == 'csv':
		cmd += '/csv_reader.R '
	elif fe == 'json':
		cmd += '/json_reader.R '
	else:
		return "{} file type is not supported. Please upload something else.".format(fe)
	cmd += filename + ' ' + fn
	import subprocess
	s = subprocess.run(cmd, check = True, stdout=subprocess.PIPE, encoding='utf-8')

	return s.stdout

def parser(csv_text_string):
    '''
    Takes a csv-formatted text string and formats it into a dictionary ready
    for JSON parsing
    
    '''
    dd = {}
    lst_of_lines = csv_text_string.split('\n')
    for i in lst_of_lines:
        lst_of_elts = i.split(',')
        dd[lst_of_elts.pop(0)] = lst_of_elts
    for (k,v) in dd.items():
        float_lst = []
        for i in v:
            float_lst.append(float(i))
        dd[k] = float_lst
    return dd

