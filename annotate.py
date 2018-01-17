# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    author: Noémi Vadász
    last update: 2017.01.17.
    VFrame searcher and its evaluation
    comparison to two other solutions:
        1. baseline: connect the nearest prev/inf to the verb (+2 restrictions)
        2. PREVERB, INF edges from magyarlanc
    after run, evaluate with eval.py
"""
from itertools import chain, islice
from collections import defaultdict
import re


def partition(list_, indices):
    i = iter(list_)
    return tuple([list(islice(i, n)) for n in chain(indices, [None])])


def prev_list():
    """
    extracts a list of preverbs from the 1st column of Manócska, sorted by length (in descending order)
    converts the list into a regular expression
    """

    prevs = set()
    exceptions = ['hív', 'tetszik', 'jön', 'tekintet', 'habozik', 'vissza-vissza', 'emlékszik', 'érzik',
                  'félt', 'z', 'y', 'ejt', 'késztet', 'mentet', 'teremt', 'hajol', 'eresztet', 'kelletik',
                  '8', 'kelt', 'hallik', 'sejtet', 'felejtet', 'elé']
    with open('manocska/manocska.txt', encoding='utf-8') as fr:
        for line in fr:
            verb = line.strip().split('\t')[0]
            if '|' in verb and verb.split('|')[0] not in exceptions:
                prevs.add(verb.split('|')[0])

    return re.compile('|'.join(sorted(prevs, reverse=True)))


def readtext():
    """
    read input file of test sentences
    sentence / line
    appends end-of-sentence characters

    :return: list of sentences
    """

    sents = []

    with open('test_data/final_test.txt', encoding='UTF-8') as infile:
        for line in infile:
            sents.append(list(chain((word.split('/', maxsplit=2) for word in line.strip().split(' ')),
                         (['#', '#', '#'], ['#', '#', '#']))))

    return sents


def readmanual():

    sentences = []
    annots = []

    with open('test_data/only_manually_annotated.txt', encoding='UTF-8') as infile:
        for sent in infile.read().split('\n%'):
            sentence, annot = sent.split('\n', maxsplit=1)
            sentences.append('%' + sentence)
            annots.append(annot.lower())

    return sentences, annots


def readdict():
    """
    read dictionary file of verb-preverb-infinitive triplets

    :return: vframe dictionary in defaultdict(dict)
    """
    vframedict = defaultdict(dict)
    # TODO: XXX Ez a manócskából kiszedhető lesz, mivel belekerül a VFrame dict generáló...
    with open('manocska/vframe_dict/vframe_to_eval', encoding='UTF-8') as infile:
        for line in infile:
            verb, prevs = line.strip().split('\t', maxsplit=1)
            vframedict[verb] = dict(elem.split(':', maxsplit=1) for elem in prevs.split(','))
    return vframedict


def get_vframe_from_dict(vframedict, verb):
    """
    check verb in vframedict
    direction: direction of search
        L:  left
        R:  right
    what: what to search
        I:  infinitive
        P:  preverb
        B:  both

    :param vframedict: dictionary of vframes
    :param verb: finite verb stem
    :return: starting direction of searcher, what does the searcher searches for, vframe of actual verb
    """
    vframe_of_verb = vframedict[verb]

    if '?' in vframe_of_verb.values():
        # Search: Left, Infinitive
        direction, what = 'L', 'I'
    elif len(vframe_of_verb) > 0:
        # Search: Left, Both infinitive and preverb
        direction, what = 'R', 'B'
    else:
        # Not in the dictionary
        direction, what = 'N', 'N'  # and empty dict

    return direction, what, vframe_of_verb


def split_prev(word, lemma, tag, ik, prev_re):
    verb = [word, lemma, tag]  # Store the preverb for the verb
    if tag.startswith('IK'):
        m = prev_re.match(lemma.lower())
        if m:
            ikl = m.group(0)
            verb = [word.lower().replace(ikl, '', 1), lemma.lower().replace(ikl, '', 1), tag]
            ik = [ikl, ikl, 'IK']
    return verb, ik


def search_inf_prev(tokens, inf_ik, inf, prev_re):
    for word, lemma, tag in tokens:
        if 'INF' in tag or 'INR' in tag:
            inf, inf_ik = split_prev(word, lemma, tag, inf_ik, prev_re)
    return inf, inf_ik


def constrain_vframe(vframe_of_verb, found_key=None, found_val=None):
    return {key: val for key, val in vframe_of_verb.items()
            if (found_key is None or key == found_key) and (found_val is None or val == found_val)}


def search_prev_in_pool(ik, pool, jth_word, vframe_of_verb):
    if len(pool) > 1:
        for word, lemma, tag in pool[-2::-1]:
            if tag == 'IK' and word != jth_word and lemma in vframe_of_verb:  # Found a good prev in the pool
                vframe_of_verb = constrain_vframe(vframe_of_verb, found_key=lemma)
                ik = [word, lemma, tag]
    return ik, vframe_of_verb


def constrain_and_set_new_direction(direction, what, vframe_of_verb, new_dir, new_what):
    vframe_of_verb = constrain_vframe(vframe_of_verb, found_val='?')
    if len(vframe_of_verb) > 1 or (len(vframe_of_verb) == 1 and 'X' not in vframe_of_verb):  # Is it still ambigous?
        direction, what = new_dir, new_what
    return direction, what, vframe_of_verb


def not_fin(tag):
    """
    checks if it is a finite verb
    true: finite
    false: inf, particle...
    :param tag:
    :return:
    """
    return 'INF' not in tag and 'INR' not in tag and 'MIB' not in tag and 'MIA' not in tag and 'HIN' not in tag and\
           'OKEP' not in tag


def search_both_in_the_window(window, direction, what, ik, inf_ik, inf, vframe_of_verb, prev_re):
    for window_word, window_lemma, window_tag in window:
        if 'INF' in window_tag or 'INR' in window_tag:  # a. subcase: found an infinitive
            inf, inf_ik = split_prev(window_word, window_lemma, window_tag, inf_ik, prev_re)
            direction, what, vframe_of_verb = constrain_and_set_new_direction(direction, what,
                                                                              vframe_of_verb, 'L', 'P')
            break
        elif window_tag == 'IK' and window_lemma in vframe_of_verb:  # b. subcase: found a preverb
            vframe_of_verb = constrain_vframe(vframe_of_verb, found_key=window_lemma)
            ik = [window_word, window_lemma, window_tag]

            if vframe_of_verb[ik[1]] == '?':
                inf, inf_ik = search_inf_prev(window, inf_ik, inf, prev_re)
            break
    # c. subcase: nothing found in the window
    else:
        direction, what = 'L', 'P'  # Proceed to Left, PreV
    return direction, what, ik, inf_ik, inf, vframe_of_verb


def vframe(sents):
    """
    vframe searcher
    iterate over sentence word-by-word
    calculate the window (+2 tokens) and the pool (previous tokens)
    analyze only finit verbs (infinitives?)
    write results to file immediately

    :param sents: list of test sentences
    :return: None
    """
    results = []

    vframedict = readdict()
    prev_re = prev_list()

    for inp_sent in sents:
        # print('%{0}'.format(' '.join(word for word, _, _ in inp_sent[:-2])), file=to_eval)

        verb = ['', ]
        ik = ['-', ]
        inf = ['-', ]
        inf_ik = ['-', ]
        j = 0

        for j, (word, lemma, tag) in enumerate(inp_sent):  # Iterate the sentence by tokens
            if word == '#':
                break

            pool, _, window, rest = partition(inp_sent[:-2], (j, 1, 2,))

            # 1. case: finite verb with a perverb on it
            # Stops at the finite verb with a preverb (not inf, inr, mib, mia, okep, hin)
            if tag.startswith('IK.IGE') and not_fin(tag):
                verb, ik = split_prev(word, lemma, tag, ik, prev_re)
                direction, what, vframe_of_verb = get_vframe_from_dict(vframedict, verb[1])

                if vframe_of_verb[ik[1]] == '?':  # Search inf to the right...
                    inf, inf_ik = search_inf_prev(chain(window, rest), inf_ik, inf, prev_re)

            # 2. case: finit verb without preverb
            # Stops at the finite verb without preverb (not inf, inr, mib, mia, okep, hin)
            elif tag.startswith('IGE') and not_fin(tag):
                verb = (word, lemma, tag)
                direction, what, vframe_of_verb = get_vframe_from_dict(vframedict, lemma)  # Check in the VFrame dict

                if direction == 'L' and what == 'I':  # Right, Both, In the pool
                    for pool_word, pool_lemma, pool_tag in pool:
                        if 'INF' in pool_tag or 'INR' in pool_tag:
                            inf, inf_ik = split_prev(pool_word, pool_lemma, pool_tag, inf_ik, prev_re)
                            direction, what, vframe_of_verb = constrain_and_set_new_direction(direction, what,
                                                                                              vframe_of_verb, 'R', 'B')
                            break
                    else:
                        direction, what = 'R', 'B'  # No inf found in the pool, next step: Search Right, Both

                # if the verb is not in the dictionary
                # elif direction == 'N' and what == 'N':
                #    verb = (word, lemma, tag)  # pass...

                if direction == 'R' and what == 'B':  # Right, Both, In the window
                    direction, what, ik, inf_ik, inf, vframe_of_verb = search_both_in_the_window(window, direction,
                                                                                                 what, ik, inf_ik, inf,
                                                                                                 vframe_of_verb,
                                                                                                 prev_re)

                if direction == 'L' and what == 'P':
                    ik, vframe_of_verb = search_prev_in_pool(ik, pool, inp_sent[j - 1][0], vframe_of_verb)

                if inf[0] == '-':  # after the constraining the still can have infinitive argument
                    if ((ik[0] != '-' and vframe_of_verb[ik[1]] == '?') or (
                                        ik[0] == '-' and 'X' in vframe_of_verb and vframe_of_verb['X'] == '?')):
                        # Search right in the rest
                        inf, inf_ik = search_inf_prev(chain(window, rest), inf_ik, inf, prev_re)

                    if ik[0] == '-':  # If there was no preverb or infinitive we search the rest of the sentence
                        for rest_word, rest_lemma, rest_tag in rest:  # for preverbs
                            if rest_tag == 'IK' and rest_lemma in vframe_of_verb:
                                ik = [rest_word, rest_lemma, rest_tag]
                                break

        # 3. case: infinitive
        if inf[0] != '-' and inf_ik[0] == '-':  # If there was an infinitive and its preverb had not been found yet
            # Adjust the window and the pool to the infintive
            pool, _, window, _ = partition(inp_sent[:-2], (inp_sent.index(inf), 1, 2,))
            direction, what, vframe_of_verb = get_vframe_from_dict(vframedict, inf[1])  # Check in the VFrame dict

            if direction == 'L' and what == 'I':  # Left, Inf, In the pool
                for pool_word, pool_lemma, pool_tag in pool:
                    if 'INF' in pool_tag or 'INR' in pool_tag:
                        # we do not save the infinitival argument itself, only note its existence
                        direction, what, vframe_of_verb = constrain_and_set_new_direction(direction, what,
                                                                                          vframe_of_verb, 'R', 'B')
                        break
                else:
                    direction, what = 'R', 'B'  # Proceed to Right, Both

            if direction == 'R' and what == 'B':  # Right, Both, In the window
                for window_word, window_lemma, window_tag in window:
                    # a. subcase: infintive is found
                    if 'INF' in window_tag or 'INR' in window_tag:
                        # we do not save the infinitival argument itself, only note its existence
                        direction, what, vframe_of_verb = constrain_and_set_new_direction(direction, what,
                                                                                          vframe_of_verb, 'L', 'P')
                        break
                    # b. subcase: preverb is found
                    elif window_tag == 'IK' and window_lemma in vframe_of_verb:
                        vframe_of_verb = constrain_vframe(vframe_of_verb, found_key=window_lemma)
                        inf_ik = [window_word, window_lemma, window_tag]
                        break
                else:
                    direction, what = 'L', 'P'  # Proceed to Left, PreV

            if direction == 'L' and what == 'P':
                inf_ik, vframe_of_verb = search_prev_in_pool(inf_ik, pool, inp_sent[j - 1][0], vframe_of_verb)

        results.append('{0}\t{1}\t{2}\t{3}'.format(ik[0].lower(), verb[0].lower(), inf_ik[0].lower(), inf[0].lower()))

    return results


def magyarlanc():
    """
    find PREVERB and INF edges in the output of magyarlanc (http://www.inf.u-szeged.hu/rgai/magyarlanc)
    :return:
    """

    results = []
    with open('temp/to_magyarlanc_out.txt', encoding='UTF-8') as infile:
        sents = infile.read().split('\n\n')
        for sent in sents:
            sent_list = [('#', '#', -1)]
            for entry in sent.split('\n'):
                _, lemma, _, wclass, ana, ind, dep_rel, *_ = entry.split('\t')
                if 'VerbForm=Fin' in ana or wclass == 'AUX':
                    dep_rel = 'FIN'
                if 'VerbForm=Inf' in ana:
                    dep_rel = 'INF'
                sent_list.append((lemma, dep_rel, int(ind)))

            fin, ik_fin, ik_inf, inf = '-', '-', '-', '-'

            for lemma, dep_rel, ind in sent_list:
                if dep_rel == 'FIN':
                    fin = lemma.lower()
                elif dep_rel == 'INF':
                    inf = lemma.lower()

            for lemma, dep_rel, ind in sent_list:
                if dep_rel == 'PREVERB':
                    prev_owner = sent_list[ind]
                    if prev_owner[1] == 'FIN' and prev_owner[0].lower() == fin:
                        ik_fin = lemma.lower()
                    elif prev_owner[1] == 'INF' and prev_owner[0].lower() == inf:
                        ik_inf = lemma.lower()
                elif dep_rel == 'INF':
                    inf_owner = sent_list[ind]
                    if inf_owner[1] == 'FIN' and inf_owner[0].lower() == fin:
                        inf = lemma.lower()

            results.append('{0}\t{1}\t{2}\t{3}'.format(ik_fin.lower(), fin.lower(), ik_inf.lower(), inf.lower()))

    return results


def baseline(sents):
    """
    article: http://people.mokk.bme.hu/~recski/pub/shallow.pdf
    connect preverb to the nearest verb
        restrict search between punctuation             DONE
        exclude auxiliaries: akar, bír, fog, kell, kezd, kíván, lehet, mer, óhajt, próbál, szabad, szándékozik, szeret,
         szokik, talál, tetszik, tud (Kálmán C.)
        exclude substantives: van                       DONE

    connect infinitive to the nearest finite verb
        restrict search between punctuation             DONE

    :param sents:
    :return:
    """

    results = []

    for inp_sent in sents:

        ik_list = []
        aux_verb_list = []
        inf_list = []
        prev_verb_list = []
        fin_verb_list = []

        aux = {'akar', 'bír', 'fog', 'kell', 'kezd', 'kíván', 'lehet', 'mer', 'óhajt', 'próbál', 'szabad',
               'szándékozik', 'szeret', 'szokik', 'talál', 'tetszik', 'tud', 'van'}

        for j, (word, lemma, tag) in enumerate(inp_sent[:-2]):

            has_ik = False
            if 'IK' in tag:
                has_ik = True

            if tag == 'IK':  # Collect IK-s
                ik_list.append((j, (word, lemma, tag)))

            elif 'IGE' in tag and not_fin(tag):  # Collect Fin-verbs aux and not aux ones...
                fin_verb_list.append((j, (word, lemma, tag), has_ik))
                aux_verb_list.append((j, (word, lemma, tag), has_ik))       # Can have INF
                if lemma not in aux:
                    prev_verb_list.append((j, (word, lemma, tag), has_ik))  # Can have PreV

            elif 'INF' in tag or 'INR' in tag:                              # Collect Inf...
                aux_verb_list.append((j, (word, lemma, tag), has_ik))       # Can have INF
                inf_list.append((j, (word, lemma, tag), has_ik))            # Can have AUX Verb
                prev_verb_list.append((j, (word, lemma, tag), has_ik))      # Can have PreV

        # Bind preverb to finite and infinite verbs by the the shortest distance (if there is no preverb on it)
        ik_verb_dict = dict()
        for ik_ind, ik in ik_list:
            min_distance = float('Inf')
            verb_min_ik = ''
            for verb_ind, verb, has_ik in prev_verb_list:
                if has_ik:
                    verb_min_ik = '-'
                else:
                    dist = abs(verb_ind - ik_ind)
                    if dist < min_distance:
                        min_distance = dist
                        verb_min_ik = verb[0]
            if verb_min_ik not in ik_verb_dict:
                ik_verb_dict[verb_min_ik] = ik[1]  # If one found we do not search for another (tie: take the left one)

        verb_inf_dict = dict()
        for inf_ind, inf, _ in inf_list:
            min_distance = float('Inf')
            inf_min_verb = ''
            for verb_ind, verb, _ in aux_verb_list:
                if inf_ind == verb_ind:
                    continue
                dist = abs(verb_ind - inf_ind)
                if dist < min_distance:
                    min_distance = dist
                    inf_min_verb = verb[0]
            if inf_min_verb not in verb_inf_dict:
                verb_inf_dict[inf_min_verb] = inf[0]

        out_line = []
        for ind, (verb, _, _), _ in fin_verb_list:
            prev_verb = ik_verb_dict.get(verb, '-')
            out_line.append('\t'.join([prev_verb.lower(), verb.lower()]))
            inf = verb_inf_dict.get(verb)
            if inf is None:
                out_line.append('\t'.join(['-', '-']))
            while inf is not None:
                prev_inf = ik_verb_dict.get(inf, '-')
                out_line.append('\t'.join([prev_inf.lower(), inf.lower()]))
                inf = verb_inf_dict.get(inf)
        results.append('\t'.join(out_line))

    return results


def print_results(sents, manual, vframe_result, magyarlanc_result, baseline_result):
    with open('temp/final_results_to_eval.txt', 'w', encoding='UTF-8') as outfile:
        for s, ma, v, m, r in zip(sents, manual, vframe_result, magyarlanc_result, baseline_result):
            print(s, ma, v, m, r, sep='\n', end='\n\n', file=outfile)


def main():
    sentlist = readtext()
    sents, manual_results = readmanual()
    vframe_results = vframe(sentlist)
    magyarlanc_results = magyarlanc()
    baseline_results = baseline(sentlist)
    print_results(sents, manual_results, vframe_results, magyarlanc_results, baseline_results)


if __name__ == '__main__':
    main()
