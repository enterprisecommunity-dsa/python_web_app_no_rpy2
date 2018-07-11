import functools
import os
import json
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
	path_to_coef = os.path.join('regression_app/reg_results', '{}_coefficients.json'.format(session['file_name_identifier']))
	with open(path_to_coef) as f:
		coef_dict = json.load(f)
	coef_list = list(coef_dict)
	intercept = coef_list.pop(0)[1]
	if request.method == 'GET':
		return render_template('prediction_entry.html')
	
	return coef_dict