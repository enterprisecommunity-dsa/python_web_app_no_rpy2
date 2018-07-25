import functools
import os
from flask import (
		Blueprint, 
		flash,
		redirect, 
		render_template,
		request,
		session,
		url_for
		)
from werkzeug.utils import secure_filename
from .R_calling_functions import lm_output_printer
bp = Blueprint('file_upload', __name__, url_prefix = '/file_upload')
UPLOAD_FOLDER = 'C:/Users/omelia/python_web_app_no_rpy2/regression_app/uploads'
ALLOWED_FILE_EXTENSIONS = set(["csv", "json"])

@bp.route('/', methods = ('GET', 'POST'))
def upload_file():
	'''
	View for uploading a file to the application. Saves the file using a secured filename in the relative
	path 'uploads/secure_filename'.
	
	Once the file is uploaded, redirects to the 'view_regression' view.
	'''
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
	

	
	
def configure_session_dict(file_name):
	'''
	Takes a file_name string and adds to the flask "session" dictionary object
	the necessary fields to point to the current file:
		'current_file_extension'
		'current_file_name_no_extension'
		'current_data_abs_path'
		'current_data_filename'
	'''
	from flask import session
	session.permanent = False
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
	'''
	The view which gives the standard R regression summary output. Calls R_calling_functions.lm_output_printer to get the summary output string, then prints it. 
	'''
	if session.get('current_data_abs_path'):
		l = lm_output_printer()
		if l == 1:
			flash("There was a problem with the text entry. Please ensure it is formatted like a csv")
			return render_template('regression_results.html', reg_output = [], fn = '')
		else:
			line_list = l.split('\n')
			filename_string = str(session['current_file_name_no_extension']+
									'.'+ session['current_file_extension'])
			
			
			
			return render_template('regression_results.html', reg_output = line_list, fn = filename_string)
		return redirect(url_for('file_upload.upload_file'))
	
	
	
	
	
	
	
