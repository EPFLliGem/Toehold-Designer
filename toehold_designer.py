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
    points = ''
    for i in range(len('UCCACAAUGUGUGGGACUUUGGCCAUUCACAUGUUUGGACUUUAGAACAGAGGAGAUAAAGAUGAAACAUGUGAAUAACCUGGCGGCAGCGCAAAAG')):
        points +='.'
    print(points)
    if(sequence != None):
        secondary_toehold = '.........................(((((((((((...(((((............)))))...)))))))))))......................'
        secondary_single = '....................................'
        window = 36
        result_path = '/home/natalija/Documents/iGEM/nupack/test_data/'
        list = nupack_analysis(sequence, secondary_toehold, secondary_single, window, result_path)

    return render_template('index.html', list=list)

@app.route('/sort', methods=['POST'])
def sort():
    list = ast.literal_eval(request.form.get('list'))
    sort_by = request.form.get('sort_by')

    if(sort_by == 'toehold'):
        list = sorted(list, key=lambda x: x[3])
    elif(sort_by == 'single'):
        list = sorted(list, key=lambda x: x[2])
    elif (sort_by == 'score'):
        list = sorted(list, key=lambda x: x[4])

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
        if no_stop(reg[0:12] + linker):
            final[reg] = rev + loop + reg[0:12] + linker

    return final

def complex_defect_score(sequence, secondary_toehold, window, result_path):
    result = {}
    sequences_list = possible_toehold(sequence, window)
    for key, value in sequences_list.items():
        file = open('{}prefix_toeh.in'.format(result_path), 'w')
        file.write("{}\n".format(value))
        file.write("{}".format(secondary_toehold))
        file.close()

        defect_toeh = 0
        count = 0
        with Popen(["complexdefect", "{}prefix_toeh".format(result_path)], stdout=PIPE) as proc:
            res = (proc.stdout.read()).decode("utf-8").split('\n')
            for l in res:
                count += 1
                if (count == 16):
                    defect_toeh = float(l)
            os.remove("{}prefix_toeh.in".format(result_path))
        result[key] = defect_toeh

    return result

def complex_defect_score_single(sequence, secondary_single, window, result_path):
    result = {}
    sequences_list = possible_toehold(sequence, window)
    for key, value in sequences_list.items():
        file = open('{}prefix_sing.in'.format(result_path), 'w')
        file.write("{}\n".format(key[0:36]))
        file.write("{}".format(secondary_single))
        file.close()

        defect_sing = 0
        count = 0
        with Popen(["complexdefect", "{}prefix_sing".format(result_path)], stdout=PIPE) as proc:
            res = (proc.stdout.read()).decode("utf-8").split('\n')
            for l in res:
                count += 1
                if (count == 16):
                    defect_sing = float(l)
            os.remove("{}prefix_sing.in".format(result_path))

        result[key] = (value, str(defect_sing))

    return result


def complex_defect_score_toehold(sequence, secondary_single, window, result_path):
    result = {}
    sequences_list = possible_toehold(sequence, window)
    for key, value in sequences_list.items():
        file = open('{}prefix_toeh_sc.in'.format(result_path), 'w')
        file.write("{}\n".format(value))
        file.write("{}".format(secondary_single))
        file.close()

        defect_sing = 0
        count = 0
        with Popen(["complexdefect", "{}prefix_toeh_sc".format(result_path)], stdout=PIPE) as proc:
            res = (proc.stdout.read()).decode("utf-8").split('\n')
            for l in res:
                count += 1
                if (count == 16):
                    defect_sing = float(l)
        #    os.remove("{}prefix_toeh_sc.in".format(result_path))

        result[key] = str(defect_sing)

    return result

def nupack_analysis(sequence, secondary_toehold, secondary_single, window, result_path):
    toehold_defect = complex_defect_score(sequence, secondary_toehold, window, result_path)
    single_trigger_defect = complex_defect_score_single(sequence, secondary_single, window, result_path)
    secondary_single = '.................................................................................................'
    single_toehold_defect = complex_defect_score_toehold(sequence, secondary_single, window, result_path)

    list_for_table = []

    for key, val in toehold_defect.items():
        score = 5 * float(single_trigger_defect[key][1]) + 4*float(single_toehold_defect[key]) + 3*float(val)
        list_for_table.append(tuple((key, single_trigger_defect[key][0], single_trigger_defect[key][1], val, score)))
    print(list_for_table)
    return list_for_table

if __name__ == '__main__':
    app.run()
