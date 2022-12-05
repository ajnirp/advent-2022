import re

# figure out how many stacks we have, and how many items the longest stack has
def parse_data(data):
    max_stack_len = 0
    for line in data:
        if line[0] == '[':
            max_stack_len += 1
        else:
            num_stacks = int(line.split()[-1])
            return num_stacks, max_stack_len

# parse the config file data into a list of stacks
def parse_config(config, num_stacks):
    stacks = [[] for i in range(num_stacks)]
    for row in config:
        i = 0
        while i < len(row):
            if row[i] == '[':
                stacks[i//4].append(row[i+1])
            i += 4
    return [[ele for ele in reversed(stack)] for stack in stacks]

def result(config):
    return ''.join(stack[-1] for stack in config)

with open('5.txt', 'r') as f:
    data = [line.strip() for line in f.readlines()]
    result_1 = 0
    result_2 = 0

num_stacks, max_stack_len = parse_data(data)

config = data[:max_stack_len]
config = parse_config(config, num_stacks)

# deep-copy the config for part 2
config2 = [[ele for ele in stack] for stack in config]

instructions = data[(max_stack_len+2):]
for instr in instructions:
    # parse the instruction
    num, src, dst = [int(n) for n in re.findall(r"\d+", instr)]
    src, dst = src-1, dst-1
    for _ in range(num):
        config[dst].append(config[src].pop())

    temp_storage = []
    for _ in range(num):
        temp_storage.append(config2[src].pop())

    for _ in range(num):
        config2[dst].append(temp_storage.pop())

print(result(config))
print(result(config2))
