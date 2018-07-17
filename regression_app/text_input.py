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
from .file_upload import ALLOWED_FILE_EXTENSIONS, UPLOAD_FOLDER, find_file_extension, configure_session_dict
bp = Blueprint('text_entry', __name__, url_prefix = '/text_entry')

@bp.route('/', methods = ('GET', 'POST'))
def import_data():
	if request.method =='POST':
		dat = request.form['data']
		
		error = None
		
		if not dat:
			error = 'Please input data.'
		if error is None:
			session_config_status = save_csv_file_for_regression(dat)
			if session_config_status == 0:
				return redirect(url_for('file_upload.view_regression'))
			else:
				flash("There was an error uploading your data. Please upload something new")
		flash(error)
	return render_template('data_import.html') 
	
	
	
def save_csv_file_for_regression(csv_like_str):
	'''
	Inputs : csv_like_str: string with formatting like a csv.
	
	Function 	1. Writes the string to a file regression_app/uploads/text_entry_data.csv
				2. Saves the appropriate fields in the session dictionary:
					'current_file_extension'
					'current_file_name_no_extension'
					'current_data_abs_path'
					'current_data_filename'
	
	'''
	with open('regression_app/uploads/text_entry_data.csv', 'w') as f:
		f.write(csv_like_str)
	session_config_status = configure_session_dict('text_entry_data.csv')
	return session_config_status
	'''
	(file_name_identifier, file_extension) = find_file_extension('text_entry_data.csv')
	session['current_file_extension'] = file_extension
	session['current_file_name_no_extension'] = file_name_identifier
	session['current_data_abs_path'] = os.path.join(UPLOAD_FOLDER, 'text_entry_data.csv')
	session['current_data_filename'] = 'text_entry_data.csv'
	'''
	

		
		
		
'''
Robots, Wheels, Worker Hours
14, 32, 100
1, 5, 12
10, 31, 120
13, 40, 110
20, 40, 200


Authors, Words, Books, Food, Whales
12, 10, 5, .3, 13
100, 123, .22, 1, 1
1, 1, 0, 0, 0
24, 70, .7, 123, 0
55, 69, .44, 89, 122
345, 44, .123, 12, 90
'''