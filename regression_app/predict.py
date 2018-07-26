import functools
import os
import json
from flask import (
		Blueprint, 
		flash,
		redirect, 
		render_template,
		request,
		session,
		url_for
		)
		
bp = Blueprint('predict', __name__, url_prefix = '/predict')

@bp.route('/', methods = ('GET', 'POST'))
def predict():
	'''
	This is the view for prediction value inputs. The function accesses a json object (containing coefficients) saved by the R process
		and populates text boxes for each coefficient. 
	The function also saves a few more fields to the "session" dictionary: a list of coefficient names, the regression intercept, 
		a list of coefficient estimates (estimated by the R process), and a list of user-given prediction inputs.
	If the inputs are all present and posted, this redirects to 'predict/show_results'
	'''
	if session.get('coefficients_json'):
		
		coef_dict = session['coefficients_json']
		coef_list = list(coef_dict.items())
		coef_names = []
		coef_estimates = []
		for i in coef_list:
			coef_names.append(i[0])
			coef_estimates.append(i[1])
		intercept = coef_names.pop(0)
		session['coef_names'] = coef_names
		session['intercept'] = coef_estimates.pop(0)
		session['coef_estimates'] = coef_estimates
		
		if request.method == 'POST':
			list_of_inputs = []
			error = ''
			for i in coef_names:
				if request.form[i] == '':
					error += '{} needs an input, '.format(i)
				else:
					try:
						float(request.form[i])
					except ValueError:
						error += '{} needs a numeric input, '.format(i)
					else:	
						list_of_inputs.append(request.form[i])
			if error != '':
				flash('Please fix the following: ' + error)
			else:
				session['list_of_inputs'] = list_of_inputs
				return redirect(url_for('predict.show_results'))
		return render_template('prediction_entry.html', 
									coef_names = coef_names,
									fn = session['current_data_filename'])
	else:
		return redirect(url_for('index'))
@bp.route('/show_results', methods = ('GET',))
def show_results():
	'''
	This view uses values stored to the session dictionary to create a prediction for the linear model. The objects it uses are 
		'list_of_inputs' : the list of user-given inputs for the prediction case
		'intercept' : the intercept of the linear model (estimated by the R process)
		'coef_estimates' : estimates of the linear model coefficients (estimated by the R process)
	'''
	if session.get('list_of_inputs'):
		input_list = []
		for i in session['list_of_inputs']:
			input_list.append(float(i))
		est = session['intercept']
		estimates = session['coef_estimates']
		for j in range(len(input_list)):
			est += input_list[j]*estimates[j]
			
		return render_template('pred_results.html', 
								fn = session['current_data_filename'],
								est = est, 
								int = session['intercept'],
								name_list = session['coef_names'],
								est_list = session['coef_estimates']
								)
	else:
		return redirect(url_for('index'))
	
	
	
	
	