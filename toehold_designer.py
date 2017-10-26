from flask import Flask, render_template, request
import ast
from utilities import *
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    sequence=request.form.get('sequence')
    list = []
    if sequence != None:
        secondary_sensor_B = '.........................(((((((((((...(((((............)))))...)))))))))))......................'
        secondary_sensor_A = '..............................(((((((((...((((((...........))))))...)))))))))..............................'
        window = 36
        result_path = '/home/natalija/Documents/iGEM/nupack/data/'
        list = sorted(nupack_analysis(sequence, secondary_sensor_A, window, 'A', result_path), key=lambda x: x[5])

    return render_template('index.html', list=list)

@app.route('/sort', methods=['POST'])
def sort():
    list = ast.literal_eval(request.form.get('list'))
    sort_by = request.form.get('sort_by')

    if(sort_by == 'target'):
        list = sorted(list, key=lambda x: x[2])
    elif(sort_by == 'toehold'):
        list = sorted(list, key=lambda x: x[3])
    elif (sort_by == 'sensor'):
        list = sorted(list, key=lambda x: x[4])
    elif (sort_by == 'score'):
        list = sorted(list, key=lambda x: x[5])

    return render_template('index.html', list=list)


if __name__ == '__main__':
    app.run()
