import functools
import os
from flask import (
		Blueprint, 
		flash,
		g,
		redirect, 
		render_template,
		request,
		session,
		url_for
		)
from werkzeug.utils import secure_filename
from .file_reading_writing import lm_output_printer
bp = Blueprint('file_upload', __name__, url_prefix = '/file_upload')
UPLOAD_FOLDER = 'C:/Users/omelia/python_web_app_no_rpy2/regression_app/uploads'
ALLOWED_FILE_EXTENSIONS = set(["csv", "json"])

@bp.route('/', methods = ('GET', 'POST'))
def upload_file():
	if request.method == 'POST':
		if 'the_file' not in request.files:
			flash("Please choose a file")
			#return redirect(url_for('upload_file'))
		
		else:
			f = request.files['the_file']
			#session['the_file'] = f 
			
			if f.filename == '':
				flash("No file selected")
				#return redirect(url_for('upload_file'))
				
			session_configuration_status = configure_session_dict(secure_filename(f.filename))
			
			if session_configuration_status == 0:
				f.save(session['current_data_abs_path'])
				return redirect(url_for('file_upload.view_regression'))
			
	return render_template('file_upload.html')
	

	
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
            dd[nums_to_headers_dict[k]].append(float(line_objs[k]))
    import json
    return json.dumps(dd, separators=(',', ':'))
	
	
def configure_session_dict(file_name):
	'''
	Takes a file_name string and adds to the flask session dictionary object
	the necessary fields to point to the current file:
		'current_file_extension'
		'current_file_name_no_extension'
		'current_data_abs_path'
		'current_data_filename'
	'''
	(file_name_identifier, file_extension) = find_file_extension(file_name)
	if file_extension not in ALLOWED_FILE_EXTENSIONS:
			flash("Only .csv and .json files are currently supported")
			return 1
	session['current_file_extension'] = file_extension
	session['current_file_name_no_extension'] = file_name_identifier
	session['current_data_filename'] = file_name
	session['current_data_abs_path'] = os.path.join(UPLOAD_FOLDER, file_name)
	
	return 0

	
def find_file_extension(filename):
	''' 
	Takes in a filename string and returns a tuple with strings 
		(file_name_no_extension, file_extension)
	'''
	fname_lst = filename.rsplit('.', 1)
	
	
	return (fname_lst[0], fname_lst[1].lower())	
	
@bp.route('/view_regression', methods = ('GET',))
def view_regression():
	if session.get('current_data_abs_path'):
		l = lm_output_printer()
		line_list = l.split('\n')
		filename_string = str(session['current_file_name_no_extension']+
								'.'+session['current_file_extension'])
		
		
		
		return render_template('regression_results.html', reg_output = line_list, fn = filename_string)
	return redirect(url_for('file_upload.upload_file'))
	
	
	
	
	
	
	
