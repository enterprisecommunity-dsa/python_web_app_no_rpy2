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
bp = Blueprint('data_import', __name__, url_prefix = '/')
UPLOAD_FOLDER = 'C:/Users/omelia/python_web_app_no_rpy2/regression_app/uploads'
UPLOADED_FILE = os.path.join(UPLOAD_FOLDER, 'current_upload')
@bp.route('/', methods = ('GET', 'POST'))
def import_data():
	if request.method =='POST':
		dat = request.form['data']
		
		error = None
		
		if not dat:
			error = 'Please input data.'
		if error is None:
			session['dat']=dat
			return redirect(url_for('data_import.view_results'))
		flash(error)
	return render_template('data_import.html') 
	
	
	
@bp.route('/view_results', methods = ('GET',))
def view_results():

	if session.get('dat'):
		from pandas import DataFrame, read_csv
		error = None
		#from . import linear_modeling_engine
		from io import StringIO
		
		
		#try:
		file_like_obj = StringIO(session['dat']) 
		del session['dat']
		x = read_csv(file_like_obj, header= None)
		
		#except ParserError:
			#return redirect(url_for('data_import.data_import'))
		
		#coef = linear_modeling_engine.call_r(x)
		
		cc = []
		
		for i in x.mean():
			cc.append(i)
		
		return render_template('view_results.html', coef=cc)
	else:
		return redirect(url_for('data_import.import_data'))

  
@bp.route('/upload', methods = ('GET', 'POST'))
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
			return redirect(url_for('data_import.view_files'))
		
	return render_template('file_upload.html')

@bp.route('/view_files', methods = ('GET',))
def view_files():
	filename_string = str(session['current_data_abs_path'])
	l = lm_output_printer(filename_string, csv=True)
	line_list = l.split('\n')
	
	return render_template('regression_results.html', reg_output = line_list)
	
	
	