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


@app.route('/home', methods=['POST'])
def home():
    list = ast.literal_eval(request.form.get('list'))
    return render_template('index.html', list=list)


@app.route('/details', methods=['POST'])
def details():
    list = ast.literal_eval(request.form.get('list'))
    index = int(request.form.get('index')) % len(list)
    element = list[index]

    target = element[0]
    toehold = element[1]
    target_ss = element[2]
    toehold_ss = element[3]
    defect = element[4]
    score = element[5]

    toeholdsB = possible_toehold_B(target, reversed_complement(target))

    return render_template('details.html', details=(target, toehold, target_ss,toehold_ss, defect, score, list, index, toeholdsB))

if __name__ == '__main__':
    app.run()
