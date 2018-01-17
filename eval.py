# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    author: Noémi Vadász
    last update: 2017.11.14.

    evaluate VFrame
    gold standard: manually annotated sentences
    print results to terminal
"""


def readtext():

    with open('temp/final_results_to_eval.txt', encoding='UTF-8') as infile:
        lines = [line.strip().split('\t') for line in infile if not line.startswith('%') and len(line) > 1]

    vframe = []
    magyarlanc = []
    recski = []

    for l in range(0, len(lines) - 1, 4):
        vframe.append((lines[l], lines[l + 1]))
        magyarlanc.append((lines[l], lines[l + 2]))
        recski.append((lines[l], lines[l + 3]))

    return vframe, magyarlanc, recski


def fix_unsplitted_good_prev(a_fin, a_prev, g_fin, g_prev, bad_verb, print_bad=True):
    if a_fin.endswith(g_fin) and a_fin.replace(g_fin, '', 1) == g_prev:
        preverb = a_fin.replace(g_fin, '', 1)
        verb = a_fin.replace(preverb, '', 1)
        a_fin = verb
        if a_prev != '-':
            a_prev += ' ' + preverb
        else:
            a_prev = preverb
    else:
        bad_verb += 1
        if print_bad:
            print(g_fin + ' ' + a_fin)
    return a_fin, a_prev, bad_verb


def count_confusions(g_verb, a_verb, g_elem, a_elem, gold, auto, tp, tp_list, tn, tn_list, fp, fp_list, fn, fn_list):
    if g_verb != a_verb:  # mismatch
        fp += 1
        fn += 1
        fp_list.append((gold, auto))
        fn_list.append((gold, auto))

    # no elem in the gold standard, no elem in the automatic annotation
    if g_elem == a_elem == '-':
        tn += 1
        tn_list.append((gold, auto))
    # both have elem and they are the same
    elif g_elem == a_elem != '-':
        tp += 1
        tp_list.append((gold, auto))
    # the gold standard has an elem, but the automatic annotation not
    elif g_elem != a_elem and a_elem == '-':
        fn += 1
        fn_list.append((gold, auto))
    # the gold standard has no elem, but the automatic annotation has
    elif g_elem != a_elem and g_elem == '-':
        fp += 1
        fp_list.append((gold, auto))
    # both have an elem, and they are not the same
    elif g_elem != a_elem and g_elem != '-' and a_elem != '-':
        fp += 1
        fn += 1
        fp_list.append((gold, auto))
        fn_list.append((gold, auto))
    return fn, fp, tn, tp


def print_result(title, tp, tn, fp, fn, rest):
    print('{0}\ntp: {1}\ntn: {2}\nfp: {3}\nfn: {4}\n{5}'.format(title, tp, tn, fp, fn, rest))


def evaluate(linepairs):

    bad_verb = 0
    bad_inf = 0

    prev_tp = 0
    prev_tp_list = []
    prev_tn = 0
    prev_tn_list = []
    prev_fp = 0
    prev_fp_list = []
    prev_fn = 0
    prev_fn_list = []

    inf_prev_tp = 0
    inf_prev_tp_list = []
    inf_prev_tn = 0
    inf_prev_tn_list = []
    inf_prev_fp = 0
    inf_prev_fp_list = []
    inf_prev_fn = 0
    inf_prev_fn_list = []

    inf_tp = 0
    inf_tp_list = []
    inf_tn = 0
    inf_tn_list = []
    inf_fp = 0
    inf_fp_list = []
    inf_fn = 0
    inf_fn_list = []

    for gold, auto in linepairs:
        g_prev, g_fin, g_infprev, g_inf = gold
        a_prev, a_fin, a_infprev, a_inf = auto[:4]
        if g_fin.lower() != a_fin.lower():
            a_fin, a_prev, bad_verb = fix_unsplitted_good_prev(a_fin, a_prev, g_fin, g_prev, bad_verb)
        if g_inf.lower() != a_inf.lower():
            a_inf, a_infprev, bad_inf = fix_unsplitted_good_prev(a_inf, a_infprev, g_inf, g_infprev, bad_inf, False)

        gold, auto = (g_prev, g_fin, g_infprev, g_inf), (a_prev, a_fin, a_infprev, a_inf)

        prev_fn, prev_fp, prev_tn, prev_tp = count_confusions(g_fin, a_fin, g_prev, a_prev, gold, auto, prev_tp,
                                                              prev_tp_list, prev_tn, prev_tn_list, prev_fp,
                                                              prev_fp_list, prev_fn, prev_fn_list)

        inf_prev_fn, inf_prev_fp, inf_prev_tn, inf_prev_tp = count_confusions(g_inf, a_inf, g_infprev, a_infprev, gold,
                                                                              auto, inf_prev_tp, inf_prev_tp_list,
                                                                              inf_prev_tn, inf_prev_tn_list,
                                                                              inf_prev_fp, inf_prev_fp_list,
                                                                              inf_prev_fn, inf_prev_fn_list)

        inf_fn, inf_fp, inf_tn, inf_tp = count_confusions(g_fin, a_fin, g_inf, a_inf, gold, auto, inf_tp, inf_tp_list,
                                                          inf_tn, inf_tn_list, inf_fp, inf_fp_list, inf_fn, inf_fn_list)

    print('No. of bad verbs: ' + str(bad_verb), end='\n\n')

    rest = '\n'.join([
                     # str(prev_tp_list),
                     # str(prev_tn_list),
                     'false positive',
                     str(prev_fp_list),
                     'false negative',
                     str(prev_fn_list), ''])

    print_result('preverb evaluation separately', prev_tp, prev_tn, prev_fp, prev_fn, rest)

    rest = '\n'.join([
                     # str(inf_prev_tp_list),
                     # str(inf_prev_tn_list),
                     'false positive',
                     str(inf_prev_fp_list),
                     'false negative',
                     str(inf_prev_fn_list), ''])

    print_result('inf preverb evaluation separately', inf_prev_tp, inf_prev_tn, inf_prev_fp, inf_prev_fn, rest)

    rest = '\n'.join([
                     # str(inf_tp_list),
                     # str(inf_tn_list),
                     'false positive',
                     str(inf_fp_list),
                     'false negative',
                     str(inf_fn_list), ''])

    print_result('inf evaluation separately', inf_tp, inf_tn, inf_fp, inf_fn, rest)

    print_result('all prev evaluation',
                 prev_tp + inf_prev_tp,
                 prev_tn + inf_prev_tn,
                 prev_fp + inf_prev_fp,
                 prev_fn + inf_prev_fn, '')

    print_result('TOTAL evaluation',
                 prev_tp + inf_prev_tp + inf_tp,
                 prev_tn + inf_prev_tn + inf_tn,
                 prev_fp + inf_prev_fp + inf_fp,
                 prev_fn + inf_prev_fn + inf_fn, '')


def main():

    print('...reading results from file to evaluate...')
    vframe, magyarlanc, recski = readtext()

    print('...evaluating VFrame...')
    evaluate(vframe)
    print('...evaluating magyarlanc...')
    evaluate(magyarlanc)
    print('...evaluating recski...')
    evaluate(recski)


if __name__ == '__main__':
    main()
