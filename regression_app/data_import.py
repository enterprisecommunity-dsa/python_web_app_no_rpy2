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
	
	
	
@bp.route('/view_results', methods = ('GET', 'POST'))
def view_results():
	import pandas as pd
	error = None
	from . import ????
	
	try:
		x = pd.DataFrame(session['dat'])
	
	except:
		return redirect(url_for('data_import.data_import'))
	