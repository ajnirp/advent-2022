# python3 5.py < 5.txt

import copy

with open(0) as file:
    lines = file.readlines()
    data = [line[:-1] for line in lines]

def config_line_idx(data):
    i = 0
    should_continue = True
    for line in data:
        if should_continue:
            for c in line:
                if c.isdigit():
                    should_continue = False
                    break
            i += 1
    return i-1

def transpose(mat):
    rows, cols = len(mat), len(mat[0])
    return [''.join(mat[r][c] for r in range(rows)) for c in range(cols)]

def init(data):
    idx = config_line_idx(data)
    config = transpose(data[:idx])
    result = []
    for line in config:
        line = line.strip()
        if line and line[0].isalpha():
            result.append(line)
    result = [[c for c in reversed(line)] for line in result]
    return result, data[idx+2:]

orig_config, instructions = init(data)

def process(orig_config, instructions, mode):
    config = copy.deepcopy(orig_config)
    for instr in instructions:
        _, num, _, src, _, dst = instr.split()
        num = int(num)
        src = int(src)-1
        dst = int(dst)-1
        if mode == 1:
            for _ in range(num):
                config[dst].append(config[src].pop())
        elif mode == 2:
            buffer = []
            for _ in range(num):
                buffer.append(config[src].pop())
            for _ in range(num):
                config[dst].append(buffer.pop())
    return ''.join(line[-1] for line in config)

print(process(orig_config, instructions, 1)) # JRVNHHCSJ
print(process(orig_config, instructions, 2)) # GNFBSBJLH
