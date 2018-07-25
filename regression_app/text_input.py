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
	'''
	View which lets user input csv-formatted data into a text box. Calls savecsv_file_for_regression to save the 
		text into regression_app/uploads/text_entry_data.csv and configure the session dictionary to point to the
		new file. 
	
	If upload is successful, redirects to 'file_upload/view_regression'
	
	'''
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


		
		
		
