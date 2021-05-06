[![forthebadge](https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg)](https://forthebadge.com)

There are a total of four problems, each of them are stated and the solutions explained in the next section.

The solution for [Problem 1](https://github.com/codelixir/automata-theory#problem-1-converting-a-regular-expression-to-an-nfa) that is discussed here discusses the Shunting-yard algorithm to convert infix expression to postfix expression. You can read more about it [here](https://en.wikipedia.org/wiki/Shunting-yard_algorithm).

Sample inputs/outputs for each code are given in the [Formats](https://github.com/codelixir/automata-theory/tree/main/Formats) directory.

These programs were written as a part of the Automata Theory course, Spring 2021.

---

## Running the scripts

```
$ python3 q1.py input.json output.json
```
You can replace q1.py by q2.py or q3.py or q4.py. <br>
input.json by path of the input file. <br>
output.json by required path of the output file. <br>

<br>
<br>

# Problem 1: Converting a Regular Expression to an NFA

### Step 1: Converting Regex from Infix representation to Postfix representation
- Add `.` to represent the concatenate operator.
- Convert expression to postfix using the Shuntinng-yard Algorithm
  
### Step 2: Converting the Postfix form of Regex to an NFA

- To do this, I defined two classes - `State` and `NFA` (an `NFA` object uses `State` objects as parameters). 
- I made a stack to store these NFAs. I would iterate through the postfix expression, character by character, and would make new NFAs (and pop older ones in some cases).
- After iterating through the whole expression, we have simplified our problem into a single NFA, which is the only element in the stack. Now we can pop it and we have our required NFA

### Step 3: Converting this NFA object to a dictionary

- I visit all `State` objects (breadth-first traversal) and through this traversal I can generate the **states** array and the **transition_function**.
- The **letters** is the set of non-epsilon letters in all the transitions in the transition function.
- The **start_states** and **end_states** could be obtained by accessing the `start` and `end` attributes of the `NFA` object.

<br><br>

# Problem 2: Converting an NFA to a DFA

- The **states** of the DFA is the power set of the states of the NFA.
- The **letters** are same as the letters of the NFA.
- The **start_states** are single-valued sets containing _only_ the start states of the NFA.
- The **final_states** are any sets which contain any of the final states of the NFA.
  
### Obtaining the transition function
- For a given DFA state and a given letter, first we find the transition results for each of the NFA states that form the DFA states.
- The union of these results gives us the transition from this start state with a given letter
- By repeating this procedure for all of the DFA states for each letter, we get the **transition_function** for the DFA.

<br><br>

# Problem 3: Converting a DFA to a Regular Expression

### Step 1: Removing Dead States
First we remove the states which are inaccessible or dead, if applicable.

### Step 2: Adding new initial and final states
In most cases, the start/end states can have multiple edges. To make conversion easier, we introduces new start and end states.
- Make a new start state (say `Qs`). Make $\epsilon$ edges from Qs to all the states which used to be start states.
- Make a new final state (say `Qf`). Make $\epsilon$ edges from the states which used to be the final states to Qf. The old accepted states are no longer accepted states now.

### Step 3: Simplifying Parallel Edges
- If there are multiple transitions from the same start state to the same end state, combine them with union operator.

### Step 4: Removing Self-Loops
- If there are self loops at any node, resolve it by using the closure operator.

### Step 5: State Elimination
- Since no self-loops are present and we have also simplified edges with union, we can start eliminating states, one by one.
- To eliminate a state Q1, let's say it has incoming edges from Qi's and outgoing edges from Qj's:
```
Qi --(E_i1)--> Q1
Q1 --(E_1j)--> Qj
```
We can change this to
```
Qi --(E_i1.E1j)--> Qj
```
for all Qi and Qj and eliminate Q1.
(`.` represents concatenation)
- Eliminating a state can lead to parallel edges and/or self loops, so we need to resolve them again at every step.

### Step 6: Obtainging the Regex:

After removing all the states other than Qs and Qf, and simplifying, we will be left with
```
Qs --(E_sf)--> Qf
```
Now `E_sf` gives us our required Regular Expression.

<br><br>

# Problem 4: Minimizing a DFA

### Step 1: Removing dead and inaccessible states
First of all, remove the states that are either never visited or never lead to an accept state

### Step 2: Applying the Equivalence Theorem
- On the resultant DFA after removing unwanted states, we can start making partitions according to the equivalence theorem.
- First, we partition our states into two sets of Final and non-Final states. 
- For the next iteration, we iterate though each set and group the states which are equivalent, and these groups represent the sets in the next partition. Here, two states are said to be equvalent if all transitions from these states are similar (i.e. have their end state in the same group).
- We repeat this process until two consecutive partitions are identical. This indicates that this partition is now the minimized form.

### Step 3: Obtaining the DFA:
- The sets obtained in the last partition are the **states** of the minimized DFA.
- The **letters** are same as that of the original DFA.
- The **start_states** are any sets containing any of the original start states.
- Similarly, the **final_states** are any sets containing any of the original final states.
- The transitions of the **transition_matrix** can be obtained by:
  - From a given set, pick any state from the original DFA (since all of them are equivalent). The set containing the resultant state is the resultant state for the transition of the minimized DFA.
  - Since the last line might sound confusing, I'll show it with an example:

Let the states of the Minimized DFA be:
```
[Q1, Q2, Q3]
[Q4, Q5]
[Q6, Q7]
```
And let 
```
Q1 --(a)--> Q4
```
be one of the transitions. Now, a transition of the new (minimized) DFA would be:
```
[Q1, Q2, Q3] --(a)--> [Q4, Q5]
```
- Repeat this for all the **states** and all the **letters** to get the **transition_matrix**
- Hence we have obtained the Minimized form of the DFA.
