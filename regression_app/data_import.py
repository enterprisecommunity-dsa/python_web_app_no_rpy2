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
		from pandas import DataFrame, read_csv
		error = None
		from . import linear_modeling_engine
		from io import StringIO
		
		
		#try:
		file_like_obj = StringIO(session['dat']) 
		del session['dat']
		x = read_csv(file_like_obj, header= None)
		
		#except ParserError:
			#return redirect(url_for('data_import.data_import'))
		
		coef = linear_modeling_engine.call_r(x)
		
		cc = []
		
		for i in coef:
			cc.append(i)
		
		return render_template('view_results.html', coef=cc)
		
		
		
def any_function_call():
	return 0
	
		
		
def second_call_r(df):
	import rpy2.robjects
	#from rpy2.robjects import pandas2ri
	from rpy2.robjects.packages import importr
	stats = importr('stats')
	base = importr('base')
	'''
	pandas2ri.activate()
	rpy2.robjects.globalenv['dataframe'] = df
	m = stats.lm('dataframe', data=base.as_symbol('dataframe'))
	return m
	'''
	
'''
12,14,15,2
0,7,4,2
12,5,5,5
1,2,3,4


'''

  
		
	
	
	