# python_web_app_no_rpy2

Creating a python web app built on the Flask framework. Runs at https://no-r-call.herokuapp.com/ 
    
regression_app: Contains the code for the app being built.
    __init__.py App initialization and configuration
    data_import.py Defines the views; runs the Python processes behind the HTML
    templates:  Contains HTML templates; written using flask's built-in templating language, Jinja2
            base.html Makes a title
            data_import.html Text entry box with instructions for data input
            view_results.html Shows the resulting linear model

Procfile    Instructs Heroku how to launch app
requirements.txt    Defines required Python packages
