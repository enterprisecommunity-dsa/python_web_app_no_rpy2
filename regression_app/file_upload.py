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
UPLOADED_FILE = os.path.join(UPLOAD_FOLDER, 'current_upload')
ALLOWED_FILE_EXTENSIONS = set(["csv", "json"])
@bp.route('/', methods = ('GET', 'POST'))
def upload_file():
	if request.method == 'POST':
		if 'the_file' not in request.files:
			flash("Please upload a file")
			return redirect(url_for('upload_file'))
			
		f = request.files['the_file']
		(file_name_identifier, file_extension) = find_file_extension(f.filename)
		session['file_extension'] = file_extension
		session['file_name_identifier'] = file_name_identifier
		if f.filename == '':
			flash("No file selected")
			return redirect(url_for('upload_file'))
		if file_extension not in ALLOWED_FILE_EXTENSIONS:
			flash("Only .csv and .json files are currently supported")
		if f:
			filename = secure_filename(f.filename)
			session['current_data_filename'] = filename
			session['current_data_abs_path'] = os.path.join(UPLOAD_FOLDER, filename)
			f.save(session['current_data_abs_path'])
			return redirect(url_for('file_upload.view_regression'))
		
	return render_template('file_upload.html')
	
	
def find_file_extension(filename):
	''' 
	Takes in a filename string and puts out a string with just the extension
	'''
	fname_lst = filename.rsplit('.', 1)
	
	
	return (fname_lst[0], fname_lst[1].lower())

@bp.route('/view_regression', methods = ('GET',))
def view_regression():
	if session.get('current_data_filename'):
		filepath_string = str(session['current_data_abs_path'])
		l = lm_output_printer(filepath_string)
		line_list = l.split('\n')
		filename_string = str(session['current_data_filename'])
		
		return render_template('regression_results.html', reg_output = line_list, fn = filename_string)
	return redirect(url_for('file_upload.upload_file'))