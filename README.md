# python_web_app

Creating a python web app built on the Flask framework. First it will run locally, then migrate to a Heroku server.

instance: Automatically populated by flask; enpty right now but would contain the SQLite database if one is initaited
    
regression_app: Contains the code for the app being built.
    __init__.py App initialization and configuration
    data_import.py Defines the views; runs the Python processes behind the HTML
    linear_modeling_engine.py Contains the script using rpy2 to call linear_modeler_function.R and running a linear regression
    linear_modeler_function.R R script read by linear_modeling_engine.py
    __pycache__:  Automatically populated by Python; contains compiled code
    templates:  Contains HTML templates; written using flask's built-in templating language, Jinja2
            base.html Makes a title
            data_import.html Text entry box with instructions for data input
            view_results.html Shows the resulting linear model
