import os
from flask import Flask, render_template

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