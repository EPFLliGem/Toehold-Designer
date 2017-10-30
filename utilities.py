import os
import os.path
from subprocess import Popen, PIPE

import time


def split_sequence(sequence, window):
    sequences = []
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

    # reverse the sequence
    return complement[::-1]


def no_stop(sequence):
    stop = ['UAA', 'UAG', 'UGA']

    for i in range(0, len(sequence), 3):
        if sequence[i:i + 3] in stop:
            return False

    return True


def possible_toehold_B(reg, rev):
    loop = 'GGACUUUAGAACAGAGGAGAUAAAGAUG'
    linker = 'AACCUGGCGGCAGCGCAAAAG'
    toeholds = []

    for n in ['A', 'G', 'U', 'C']:
        if no_stop(reg[0:11] + n + linker):
            toeholds.append(rev + loop + reg[0:11] + n + linker)

    return toeholds

def possible_toehold_A(reg_sequences, rev_comp_sequences):
    loop = 'GUUAUAGUUAUGAACAGAGGAGACAUAACAUGAAC'
    linker = 'GUUAACCUGGCGGCAGCGCAAAAG'
    toeholds = {}

    for rev, reg in zip(rev_comp_sequences, reg_sequences):
        if no_stop(reg[0:6] + 'AAC' + reversed_complement(reg[0:3]) + linker):
            toeholds[reg] = rev + loop + reg[0:6] + 'AAC' + reversed_complement(reg[0:3]) + linker

    return toeholds

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


def single_streadness(sequence, result_path, wait=1):
    file = open('{}pipo.in'.format(result_path), 'w')
    file.write("{}\n".format(sequence))
    file.close()

    Popen(["pairs", "{}pipo".format(result_path)], stdout=PIPE)
    time.sleep(wait)
    with open("{}pipo.ppairs".format(result_path)) as res:
        parsed_res = parse_pairs_result(res, len(sequence))

    os.remove("{}pipo.ppairs".format(result_path,))
    os.remove("{}pipo.in".format(result_path))


    return parsed_res


def parse_pairs_result(res, length):
    final = []
    for r in res:
        r = r.strip('\n')
        if not r.startswith('%'):
            r = r.split('\t')
            if len(r) == 3:
                if r[1] == str(length+1):
                    final.append(float(r[2]))

    return final

def nupack_analysis(sequence, secondary_sensor,  window, sensor_type, result_path):
    list_for_table = []

    processed_sequence = sequence.upper().replace('T', 'U').replace(' ', '')
    reg_sequences = split_sequence(processed_sequence, window)
    rev_comp_sequences = [reversed_complement(s) for s in reg_sequences]

    if sensor_type == 'A':
        target_toehold_map = possible_toehold_A(reg_sequences, rev_comp_sequences)
    else:
        target_toehold_map = possible_toehold_B(reg_sequences, rev_comp_sequences)

    sequence = sequence.upper().replace('T', 'U')
    single_streadness_sequence = single_streadness(sequence, result_path, wait=6)
    for target, toehold in target_toehold_map.items():
        id = sequence.index(target)

        target_defect = sum(single_streadness_sequence[id:id+36])/36
        toehold_defect = sum(single_streadness(toehold, result_path)[0:30])/30
        sensor_defect = complex_defect(toehold, secondary_sensor, result_path)

        score = 5*(1-target_defect) + 4*(1-toehold_defect) + 3*sensor_defect

        list_for_table.append(tuple([target[0:36], toehold, 1-target_defect, 1-toehold_defect, sensor_defect, score]))

    return list_for_table