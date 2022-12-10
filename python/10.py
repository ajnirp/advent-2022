def update(cycle, crt, x):
    pos = cycle - 1
    row = pos // 40
    col = pos % 40
    if col in [x-1, x, x+1]:
        crt[row][col] = '#'

def process(instructions):
    interesting = [20 + 40*i for i in range(6)]
    result, idx, x, cycle = 0, 0, 1, 1

    for instr in instructions:
        if idx == len(interesting):
            return result
        if cycle == interesting[idx]:
            result += interesting[idx] * x
            idx += 1
        if instr[0] == 'n':
            cycle += 1
            continue
        else:
            if idx == len(interesting):
                return result
            if cycle + 2 > interesting[idx]:
                result += interesting[idx] * x
                idx += 1
            val = int(instr.split()[-1])
            cycle += 2
            x += val
    return result

def render(instructions):
    x, cycle = 1, 1
    crt = [['.' for _ in range(40)] for _ in range(6)]
    for instr in instructions:
        if instr[0] == 'n':
            update(cycle, crt, x)
            cycle += 1
            continue
        else:
            update(cycle, crt, x)
            cycle += 1
            update(cycle, crt, x)
            cycle += 1
            val = int(instr.split()[-1])
            x += val
    for row in crt:
        print(''.join(row))


with open('../data/10.txt', 'r') as f:
    instructions = [line.strip() for line in f.readlines()]
    print(process(instructions))
    render(instructions)
