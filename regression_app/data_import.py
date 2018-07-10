import functools

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
	

bp = Blueprint('data_import', __name__, url_prefix = '/')

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

  
@bo.route('/upload', methods = ('GET', 'POST'))
def upload_file():
	if request.method == 'POST':
		f = request.files['the_file']
		file_string = f.read()
		return redirect(url_for('data_import.view_file'), file_string = file_string)
		
	return render_template('upload_file.html')

@bp.route('/view_files', methods = ('GET',))
def view_files(file_string);
	return render_template('view_files.html', file_string = file_string)
		
	
	
	