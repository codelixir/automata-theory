#!/usr/bin/env python
# coding: utf-8

# MINIMISE A DFA


import json
import sys


def resolve_dead(delta, states):
    check = {}
    for state in states:
        check.update({state: False})
    for state in DFA['start_states']:
        check[state] = True
    for edge in delta:
        check[edge[2]] = True
    return [edge for edge in delta if check[edge[0]]], [state for state in check if check[state]]


def visit(state, check, delta):
    if check[state]:
        return
    check[state] = True
    for s in [edge[2] for edge in delta if edge[0] == state]:
        visit(s, check, delta)


def resolve_inaccessible(delta, states):
    check = {}
    for state in states:
        check.update({state: False})
    for state in DFA['start_states']:
        visit(state, check, delta)
    return [edge for edge in delta if check[edge[0]]], [state for state in check if check[state]]


def equivalent(state1, state2, arr):
    check = {l: False for l in DFA['letters']}
    for l in alpha_delta:
        newlist = [edge for edge in alpha_delta[l]
                   if (edge[0] in [state1, state2])]
        if not newlist:
            check[l] = True
        elif len(newlist) == 1:
            return False
        else:
            final1, final2 = newlist[0][2], newlist[1][2]
            for group in arr:
                if final1 in group and final2 in group:
                    check[l] = True
                    break
                elif final1 in group or final2 in group:
                    return False
    if set(check.values()) == {True}:
        return True
    return False


def k_equivalence(delta, k, hist):
    partition = []
    if k == 0:
        partition.append(DFA['final_states'])
        partition.append(
            [s for s in valid_states if s not in DFA['final_states']])
        hist.append(partition)

        return False
    else:
        old_partition = hist[-1]
        for group in old_partition:
            for state in group:
                if state in [s for grp in partition for s in grp]:
                    continue
                newgrp = [state]
                for s in group:
                    if s == state:
                        continue
                    if equivalent(state, s, old_partition):
                        newgrp.append(s)
                partition.append(newgrp)
        hist.append(partition)

        if sorted(hist[-1]) == sorted(hist[-2]):
            return True
        else:
            return False


if __name__ == '__main__':

    with open(sys.argv[1], 'r') as f:
        DFA = json.load(f)

    delta = DFA['transition_function'].copy()
    delta, valid_states = resolve_dead(delta, DFA['states'])
    delta, valid_states = resolve_inaccessible(delta, valid_states)
    alpha_delta = {l: [edge for edge in delta if edge[1] == l]
                   for l in DFA['letters']}

    k = 0
    hist = []
    flag = False
    while not flag:
        flag = k_equivalence(delta, k, hist)
        k += 1

    new_states = hist[-1]

    start_states = []
    for state in new_states:
        for s in DFA['start_states']:
            if s in state:
                start_states.append(state)
                break

    final_states = []
    for state in new_states:
        for s in DFA['final_states']:
            if s in state:
                final_states.append(state)
                break

    new_delta = []
    for state in new_states:
        for l in DFA['letters']:
            endstate = [edge[2]
                        for edge in alpha_delta[l] if edge[0] == state[0]]
            if not endstate:
                continue
            for s in new_states:
                if endstate[0] in s:
                    accept = s
                    break
            new_delta.append([state, l, accept])

    minDFA = {
        'states': new_states,
        'letters': DFA['letters'],
        'transition_matrix': new_delta,
        'start_states': start_states,
        'final_states': final_states,
    }

    output = json.dumps(minDFA, indent=4)
    with open(sys.argv[2], 'w') as f:
        f.write(output)
