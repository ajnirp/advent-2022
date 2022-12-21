#!/usr/bin/python3

from copy import deepcopy

monkeys, equations = {}, {}

def evaluate(operand, monkeys, equations):
    if type(operand) == int:
        return operand
    if operand in monkeys:
        return monkeys[operand]
    if operand not in equations:
        return None
    operator, m1, m2 = equations[operand]
    m1 = evaluate(m1, monkeys, equations)
    m2 = evaluate(m2, monkeys, equations)
    if m1 is None or m2 is None:
        return None
    value = 0
    if operator == '+':
        value = m1 + m2
    elif operator == '-':
        value = m1 - m2
    elif operator == '*':
        value = m1 * m2
    elif operator == '/':
        value = m1 // m2
    monkeys[operand] = value
    return value

with open('../data/21.txt', 'r') as file:
    data = [line.strip() for line in file.readlines()]

for line in data:
    split = line.split()
    monkey = split[0][:-1]
    if len(split) == 2:
        monkeys[monkey] = int(split[1])
    else:
        equations[monkey] = (split[2], split[1], split[3])

# Part 1
monkeys_copy = deepcopy(monkeys)
print(evaluate('root', monkeys_copy, equations))

def solve(node, target, monkeys):
    if node == 'humn':
        return target
    left, right = equations[node][1], equations[node][2]
    unknown = left
    e1 = evaluate(left, monkeys, equations)
    e2 = evaluate(right, monkeys, equations)
    known = e1 if e1 else e2
    unknown = right if e1 else unknown
    operator = equations[node][0]
    if operator == '+':
        return solve(unknown, target - known, monkeys)
    elif operator == '*':
        return solve(unknown, target // known, monkeys)
    elif operator == '-':
        if unknown == left:
            return solve(unknown, known + target, monkeys)
        elif unknown == right:
            return solve(unknown, known - target, monkeys)
    elif operator == '/':
        if unknown == left:
            return solve(unknown, known * target, monkeys)
        elif unknown == right:
            return solve(unknown, known // target, monkeys)

monkeys_copy = deepcopy(monkeys)
del monkeys_copy['humn']
e1 = evaluate(equations['root'][1], monkeys_copy, equations)
e2 = evaluate(equations['root'][2], monkeys_copy, equations)
unknown = equations['root'][1]
target = e1 if e1 else e2
unknown = equations['root'][2] if e1 else unknown

# Part 2
print(solve(unknown, target, monkeys_copy))
