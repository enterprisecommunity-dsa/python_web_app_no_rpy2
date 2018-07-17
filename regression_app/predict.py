import functools
import os
import json
from numpy import array, dot
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
		
bp = Blueprint('predict', __name__, url_prefix = '/predict')

@bp.route('/', methods = ('GET', 'POST'))
def predict():
	path_to_coef = os.path.join('regression_app/reg_results', '{}_coefficients.json'.format(session['current_file_name_no_extension']))
	with open(path_to_coef) as f:
		coef_dict = json.load(f)
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
				error += '{}, '.format(i)
			list_of_inputs.append(request.form[i])
		if error != '':
			flash('The following inputs are needed: ' + error)
		else:
			session['list_of_inputs'] = list_of_inputs
			return redirect(url_for('predict.show_results'))
	return render_template('prediction_entry.html', 
								coef_names = coef_names,
								fn = session['current_data_filename'])
		
@bp.route('/show_results', methods = ('GET',))
def show_results():	
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

	
	
	
	
	