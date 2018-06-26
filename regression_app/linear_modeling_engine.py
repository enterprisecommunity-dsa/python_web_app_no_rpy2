'''
Creates a function which, given a Pandas DataFrame, calls an R script and 
returns the coefficients of a linear model. 
'''


def call_r(df):
    '''
    Arguments:
        df: A Pandas DataFrame object. The observations for the dependent
            variable MUST be in the FIRST COLUMN
    
    Returns: an rpy2 Robject float vector which stores the coefficients of the
        linear regression
    '''
    
    from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
    from rpy2.robjects import pandas2ri
    pandas2ri.activate()
    
    with open('linear_modeler_function.R') as f:
        str = f.read()
        
    mod = SignatureTranslatedAnonymousPackage(str, 'mod')
    a = mod.linear_modeler(df)
    return a