#!/usr/bin/env python
# coding: utf-8

# In[1]:


# CONVERT A REGEX TO NFA

import json
import sys


# In[2]:


# STEP ONE: Converting Regex to postfix


# In[3]:


def add_concat(regex):
    new_regex = regex[0]
    for i in range(len(regex)-1):
        c1 = regex[i]
        c2 = regex[i+1]
        if c1 not in ['+', '('] and c2 not in ['*', ')', '+']:
            new_regex += '.'
        new_regex += c2

    return new_regex


# In[4]:


def shunting(regex):
    shunt = []
    stack = []
    optr = ['*', '.', '+']
    for ch in regex:
        if ch in optr:
            while stack:
                c2 = stack[-1]
                if c2 == '(' or optr.index(c2) > optr.index(ch):
                    break
                else:
                    stack.pop()
                    shunt.append(c2)
            stack.append(ch)
        elif ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack and stack[-1] != '(':
                ch = stack.pop()
                shunt.append(ch)
            if stack[-1] == '(':
                stack.pop()
        else:  # letter
            shunt.append(ch)
    while stack:
        ch = stack.pop()
        shunt.append(ch)

    return ''.join(shunt)


# In[5]:


def postfix(infix):
    new_regex = add_concat(infix)
    return shunting(new_regex)


# In[6]:


# STEP TWO: Converting postfix regex to NFA


# In[7]:


i = 0


# In[8]:


class State:
    def __init__(self, edge1=None, edge2=None):
        global i
        self.token = '$'
        self.edge1 = edge1
        self.edge2 = edge2
        self.name = 'Q' + str(i)
        i += 1


class NFA:
    def __init__(self, start, final):
        self.start = start
        self.final = final


# In[9]:


def closure(stack):
    nfa1 = stack.pop()

    new_final = State()
    new_start = State(nfa1.start, new_final)

    nfa1.final.edge1 = nfa1.start
    nfa1.final.edge2 = new_final

    new_nfa = NFA(new_start, new_final)
    stack.append(new_nfa)


# In[10]:


def union(stack):
    nfa1 = stack.pop()
    nfa2 = stack.pop()

    new_start = State(nfa1.start, nfa2.start)
    new_final = State()

    nfa1.final.edge1 = new_final
    nfa2.final.edge1 = new_final

    new_nfa = NFA(new_start, new_final)
    stack.append(new_nfa)


# In[11]:


def concatenate(stack):
    nfa2 = stack.pop()
    nfa1 = stack.pop()

    nfa1.final.edge1 = nfa2.start

    new_start = nfa1.start
    new_final = nfa2.final

    new_nfa = NFA(new_start, new_final)
    stack.append(new_nfa)


# In[12]:


def symbol(stack, token):
    final = State()
    start = State(final)
    start.token = token
    new_nfa = NFA(start, final)
    stack.append(new_nfa)


# In[13]:


def toNFA(postex):
    stack = []
    for ch in postex:
        if ch == '*':
            closure(stack)
        elif ch == '+':
            union(stack)
        elif ch == '.':
            concatenate(stack)
        else:
            symbol(stack, ch)

    return stack[0]


# In[19]:


def visit(state, states, delta):
    if state.name in states:
        return
    states.append(state.name)
    if state.edge1:
        delta.append([state.name, state.token, state.edge1.name])
        visit(state.edge1, states, delta)
    if state.edge2:
        delta.append([state.name, '$', state.edge2.name])
        visit(state.edge2, states, delta)


# In[20]:


def traverse(nfa):
    states = []
    delta = []
    visit(nfa.start, states, delta)
    return states, delta


# In[21]:


def alphabet(delta):
    letters = list(set(edge[1] for edge in delta))
    letters.remove('$')
    return letters


# In[22]:


def convert_dict(nfa):
    states, delta = traverse(nfa)
    result = {
        'states': states,
        'letters': alphabet(delta),
        'transition_function': delta,
        'start_states': [nfa.start.name],
        'final_states': [nfa.final.name]
    }
    return result


# In[23]:


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        inp = json.load(f)

    regex = inp['regex']
    postex = postfix(regex)
    nfa = toNFA(postex)
    parsed = convert_dict(nfa)

    output = json.dumps(parsed, indent=4)
    with open(sys.argv[2], 'w') as f:
        f.write(output)

# In[ ]:
