import os
from flask import Flask, render_template

 

'''
def create_app( test_config=None, *args, **kwargs):
	app = Flask(__name__, instance_relative_config = True)
	app.config.from_mapping(
		SECRET_KEY = 'dev',
		DATABASE=os.path.join(app.instance_path, 'regression_app.sqlite')
	)
	
	if test_config is None:
		app.config.from_pyfile('config.py', silent = True)
	else:
		app.config.from_mapping(test_config)
	
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
	
	@app.route('/hello')
	def hello():
		return 'Hello, World!'


	from . import data_import
	app.register_blueprint(data_import.bp)
	
	
	return app
'''
	
	
app = Flask(__name__)
app.config.from_mapping(
		SECRET_KEY = 'dev',
		DATABASE=os.path.join(app.instance_path, 'regression_app.sqlite'),
		UPLOAD_FOLDER = 'C:/Users/omelia/python_web_app/no_rpy2/regression_app/uploads'
		
	)

from . import text_input
app.register_blueprint(text_input.bp)

from . import file_upload
app.register_blueprint(file_upload.bp)

from . import predict
app.register_blueprint(predict.bp)

@app.route('/', methods = ('GET',))
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()