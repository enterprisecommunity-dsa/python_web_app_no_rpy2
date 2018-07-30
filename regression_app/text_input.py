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
	
	If upload is successful, redirects to 'file_upload/choose_coefficients'
	
	'''
	if request.method =='POST':
		data = request.form['data']
		
		error = None
		
		if not data:
			error = 'Please input data.'
		if error is None:
			session['current_data'] = data
			session_config_status = configure_session_dict('Text entry.csv')
			if session_config_status == 0:
				return redirect(url_for('file_upload.choose_coefficients'))
			else:
				flash("There was an error uploading your data. Please upload something new")
		flash(error)
	return render_template('data_import.html') 



		
		
		
