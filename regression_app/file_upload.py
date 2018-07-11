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

@bp.route('/', methods = ('GET', 'POST'))
def upload_file():
	if request.method == 'POST':
		if 'the_file' not in request.files:
			flash("Please upload a file")
			return redirect(url_for('upload_file'))
			
		f = request.files['the_file']
		if f.filename == '':
			flash("No file selected")
			return redirect(url_for('upload_file'))
		if f:
			filename = secure_filename(f.filename)
			session['current_data_filename'] = filename
			session['current_data_abs_path'] = os.path.join(UPLOAD_FOLDER, filename)
			f.save(session['current_data_abs_path'])
			return redirect(url_for('file_upload.view_files'))
		
	return render_template('file_upload.html')

@bp.route('/view_files', methods = ('GET',))
def view_files():
	filepath_string = str(session['current_data_abs_path'])
	l = lm_output_printer(filepath_string, csv=True)
	line_list = l.split('\n')
	filename_string = str(session['current_data_filename'])
	
	return render_template('regression_results.html', reg_output = line_list, fn = filename_string)