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
#				f.save(session['current_data_abs_path'])
				session['current_data'] = str(f.read())
				return redirect(url_for('file_upload.choose_coefficients'))
			
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
#	session['current_file_extension'] = file_extension
#	session['current_file_name_no_extension'] = file_name_identifier
	session['current_data_filename'] = file_name
#	session['current_data_abs_path'] = os.path.join(UPLOAD_FOLDER, file_name)
	
	return 0

	
def find_file_extension(filename):
	''' 
	Takes in a filename string and returns a tuple with strings 
		(file_name_no_extension, file_extension)
	'''
	fname_lst = filename.rsplit('.', 1)
	
	
	return (fname_lst[0], fname_lst[1].lower())	
	
	
	
@bp.route('/choose_coefficients', methods = ('GET', 'POST'))
def choose_coefficients():
	'''
	This view populates a checklist from which users can choose one variable as the dependent variable. 
	'''
	coefficient_list = find_coefficients(session['current_data'])
	if request.method == 'POST':
		if request.form.get('selected_variable'):
			session['current_dependent_variable'] = request.form['selected_variable']
			return redirect(url_for('file_upload.view_regression'))
	else:
		flash("Please choose a variable")
	
	
	return render_template('coefficient_selection.html',
							coefficient_list = coefficient_list,
							fn = session['current_data_filename'])
	
	
	
def find_coefficients(csv_like_str):
	'''
	This is a helper function which takes the headers of the csv-like string and create a list of the column headers
	'''
	first_line = csv_like_str.split('\n')[0]
	coefficient_list = first_line.split(',')
	for i in range(len(coefficient_list)):
		coefficient_list[i] = coefficient_list[i].strip().replace(' ', '.')
	return coefficient_list
	
	
@bp.route('/view_regression', methods = ('GET',))
def view_regression():
	'''
	The view which gives the standard R regression summary output. Calls R_calling_functions.lm_output_printer to get the summary output string, then prints it. 
	'''
	if session.get('current_data'):
		l = lm_output_printer()
		if l == 1:
			flash("There was a problem with the text entry. Please ensure it is formatted like a csv")
			return render_template('regression_results.html', reg_output = [], fn = '')
		else:
			line_list = l.split('\n')
			
			# The penultimate line of stdout expected from R is a JSON-formatted string with the coefficients of the regression. 
			import json
			line_list.pop()
			session['coefficients_json'] = json.loads(line_list.pop())
			
			return render_template('regression_results.html', reg_output = line_list, fn = session['current_data_filename'])
		return redirect(url_for('file_upload.upload_file'))
	
	
	
	
	
	
	
