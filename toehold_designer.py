from flask import Flask, render_template, request
import os
from subprocess import Popen, PIPE
from collections import OrderedDict
import ast

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    sequence=request.form.get('sequence')
    list = []
    if sequence != None:
        secondary_sensor = '.........................(((((((((((...(((((............)))))...)))))))))))......................'
        secondary_toehold = '.................................................................................................'
        secondary_target = '....................................'
        window = 36
        result_path = '/home/natalija/Documents/iGEM/nupack/test_data/'
        list = nupack_analysis(sequence, secondary_toehold, secondary_target, secondary_sensor,  window, result_path)

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



def split_sequence(sequence, window):
    sequences = []
    # Keep this limit to avoid splitting to sequences
    # shorter than window
    limit = len(sequence) - window + 1
    for i in range(0, limit):
        sequences.append(sequence[i:window + i])

    return sequences


def reversed_complement(sequence):
    mapping = {'A': 'U', 'G': 'C', 'U': 'A', 'C': 'G'}
    sequence_upper = sequence.upper()

    complement = ''
    for c in sequence_upper:
        complement += mapping[c]

    return complement[::-1]


def no_stop(sequence):
    stop = ['UAA', 'UAG', 'UGA']

    for i in range(0, len(sequence), 3):
        if sequence[i:i + 3] in stop:
            return False

    return True


def possible_toehold(sequence, window):
    processed_sequence = sequence.upper().replace('T', 'U').replace(' ', '')
    reg_sequences = split_sequence(processed_sequence, window)
    rev_comp_sequences = [reversed_complement(s) for s in reg_sequences]
    loop = 'GGACUUUAGAACAGAGGAGAUAAAGAUG'
    linker = 'AACCUGGCGGCAGCGCAAAAG'
    final = {}

    for rev, reg in zip(rev_comp_sequences, reg_sequences):
        for n in ['A', 'U', 'C', 'G']:
            if no_stop(reg[0:11] + n + linker):
                final[reg+n] = rev + loop + reg[0:11] + n + linker

    return final

def complex_defect(sequence, secondary, result_path):
    file = open('{}toeh.in'.format(result_path), 'w')
    file.write("{}\n".format(sequence))
    file.write("{}".format(secondary))
    file.close()

    defect_toeh = 0
    count = 0
    with Popen(["complexdefect", "{}toeh".format(result_path)], stdout=PIPE) as proc:
        res = (proc.stdout.read()).decode("utf-8").split('\n')
        for l in res:
            count += 1
            if count == 16:
                defect_toeh = float(l)
    os.remove("{}toeh.in".format(result_path))
    return defect_toeh

def nupack_analysis(sequence, secondary_toehold, secondary_target, secondary_sensor,  window, result_path):
    list_for_table = []
    target_tohold_map = possible_toehold(sequence, window)
    count = 0

    for target, toehold in target_tohold_map.items():
        target_defect = complex_defect(target[0:36], secondary_target, result_path)
        toehold_defect = complex_defect(toehold, secondary_toehold, result_path)
        sensor_defect =  complex_defect(toehold, secondary_sensor, result_path)

        score = 5*target_defect + 4*toehold_defect+ 3*sensor_defect
        list_for_table.append(tuple([target[0:36], toehold, target_defect, toehold_defect, sensor_defect, score]))
        count += 1
        print('{} out of {}'.format(count, len(target_tohold_map)))
    return list_for_table

if __name__ == '__main__':
    app.run()
