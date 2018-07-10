'''
import os
import json
os.chdir('C:/Users/omelia/Documents/R_scripts')
cmd = 'Rscript command_line_practice.R sample_csv.csv'
import subprocess
s = subprocess.run(cmd, check = True, stdout=subprocess.PIPE, encoding='utf-8')

print(s.stdout)

cmdnew = 'Rscript command_line_practice.R Dogs, HorseShoe, Grades \n 1,2,3 \n 4,4,4 \n 0,-1, 0 \n 12,11,100'
s1 = subprocess.run(cmd, check = True, stdout = subprocess.PIPE, encoding = 'utf-8')
print(s1.stdout)
'''


def lm_output_printer(filename):
    '''
    Given a filename or relative file path, this function makes an explicit R
    call and returns the printed summary of a linear model
    '''
    
    cmd = 'Rscript command_line_practice.R '
    cmd += filename
    import subprocess
    s = subprocess.run(cmd, check = True, stdout=subprocess.PIPE, encoding='utf-8')

    return s.stdout

def parser(csv_text_string):
    '''
    Takes a csv-formatted text string and formats it into a dictionary ready
    for JSON parsing
    
    '''
    dd = {}
    lst_of_lines = csv_text_string.split('\n')
    for i in lst_of_lines:
        lst_of_elts = i.split(',')
        dd[lst_of_elts.pop(0)] = lst_of_elts
    for (k,v) in dd.items():
        float_lst = []
        for i in v:
            float_lst.append(float(i))
        dd[k] = float_lst
    return dd

