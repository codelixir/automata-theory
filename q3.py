#!/usr/bin/env python
# coding: utf-8


# CONVERT DFA TO REGEX

import json
import sys

with open(sys.argv[1], 'r') as f:
    DFA = json.load(f)


def join(string1, string2):
    if string1 == '$':
        return string2
    if string2 == '$':
        return string1
    return string1 + string2


# remove dead states

def resolve_dead(delta):
    check = {}
    for state in DFA['states']:
        check.update({state: False})
    for state in DFA['start_states']:
        check[state] = True
    for edge in delta:
        check[edge[2]] = True
    return [edge for edge in delta if check[edge[0]]], [state for state in check if check[state]]


# simplifty parallel edges

def resolve_parallel(delta):
    hist = []
    n = len(delta)
    for i in range(n):
        for j in range(i+1, n):
            if delta[i][0] == delta[j][0] and delta[i][2] == delta[j][2]:
                new_edge = [
                    delta[i][0], '(' + delta[i][1] + '+' + delta[j][1] + ')', delta[i][2]]
                delta.remove(delta[j])
                delta.append(new_edge)
                hist.append(delta[i])
                i += 1
    for old_edge in hist:
        if old_edge in delta:
            delta.remove(old_edge)
    return delta


# removing self-loops

def resolve_selfloops(delta):
    loops = []
    for edge in delta[:]:
        if edge[0] == edge[2]:
            loops.append(edge)
            delta.remove(edge)
    for loop in loops:
        for i, edge in enumerate(delta):
            if loop[0] == edge[0]:
                delta[i][1] = join('(' + loop[1] + ')*', edge[1])
    return delta


def remove_state(state, delta):
    incoming = [edge for edge in delta if edge[2] == state]
    outgoing = [edge for edge in delta if edge[0] == state]
    for edge in (incoming + outgoing):
        delta.remove(edge)
    for inedge in incoming:
        for outedge in outgoing:
            edge = [inedge[0], join(inedge[1], outedge[1]), outedge[2]]
            delta.append(edge)
    delta = resolve_parallel(delta)
    delta = resolve_selfloops(delta)
    return delta


if __name__ == '__main__':
    delta = DFA['transition_function'].copy()

    # STEP ZERO: remove dead states

    delta, valid_states = resolve_dead(delta)

    # STEP ONE: NEW INITIAL AND FINAL STATES

    start = 'Qs'
    final = 'Qf'

    for s in DFA['start_states']:
        delta.append([start, '$', s])
    for f in DFA['final_states']:
        delta.append([f, '$', final])

    # STEP TWO: simplify parallel edges

    delta = resolve_parallel(delta)

    # STEP THREE: removing self-loops

    delta = resolve_selfloops(delta)

    for state in valid_states:
        delta = remove_state(state, delta)

    regex = {'regex': delta[0][1]}
    output = json.dumps(regex, indent=4)
    with open(sys.argv[2], 'w') as f:
        f.write(output)
