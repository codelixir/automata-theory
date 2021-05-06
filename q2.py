#!/usr/bin/env python
# coding: utf-8


# CONVERT NFA TO DFA

import json
import sys

with open(sys.argv[1], 'r') as f:
    NFA = json.load(f)


# getting resultant states from NFA


def transition(state, letter):
    result = []
    for trans in NFA['transition_function']:
        if trans[0] == state and trans[1] == letter:
            result.append(trans[2])
    return result


# getting new states

def powerset(states):
    n = len(states)
    new_states = []
    for i in range(1 << n):
        new_states.append([states[k] for k in range(n) if (i & (1 << k))])
    return new_states


# getting sets containing given state

def containing(states):
    power_set = powerset(NFA['states'])
    power_sub = []
    for s in states:
        power_sub += [p for p in power_set if (s in p)
                      and (p not in power_sub)]
    return power_sub


# making state transition for DFA

def new_transition(new_state, letter):
    new_result = []
    for s in new_state:
        new_result += transition(s, letter)
    return list(set(new_result))


# making transition function for DFA

def new_function(new_states, letters=NFA['letters']):
    delta = []
    for state in new_states:
        for l in letters:
            delta.append([state, l, new_transition(state, l)])
    return delta


if __name__ == '__main__':

    new_states = powerset(NFA['states'])
    DFA = {'states': new_states,
           'letters': NFA['letters'],
           'transition_function': new_function(new_states),
           'start_states': [NFA['start_states']],
           'final_states': containing(NFA['final_states'])}

    output = json.dumps(DFA, indent=4)
    with open(sys.argv[2], 'w') as f:
        f.write(output)
