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
