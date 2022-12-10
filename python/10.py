ADDX_LEN = 2 # length of an addx cycle

def update(cycle, crt, x):
    pos = cycle - 1
    row = pos // 40
    col = pos % 40
    if col in [x-1, x, x+1]:
        crt[row][col] = '#'

def part1(instructions):
    checkpoint = [20 + 40*i for i in range(6)]
    result, idx, x, cycle = 0, 0, 1, 1

    for instr in instructions:
        # If we've finished all our checkpoints, return.
        if idx == len(checkpoint):
            return result
        # We're at a checkpoint. Increase result.
        if cycle == checkpoint[idx]:
            result += checkpoint[idx] * x
            idx += 1
        if instr[0] == 'n':
            cycle += 1
            continue
        else:
            # If we've finished all our checkpoints, return.
            if idx == len(checkpoint):
                return result
            # We're going to cross a checkpoint. Increase result.
            if cycle + ADDX_LEN > checkpoint[idx]:
                result += checkpoint[idx] * x
                idx += 1
            val = int(instr.split()[-1])
            cycle += ADDX_LEN
            x += val
    return result

def part2(instructions):
    x, cycle = 1, 1
    crt = [['.' for _ in range(40)] for _ in range(6)]
    for instr in instructions:
        if instr[0] == 'n':
            update(cycle, crt, x)
            cycle += 1
            continue
        else:
            for _ in range(ADDX_LEN):
                update(cycle, crt, x)
                cycle += 1
            val = int(instr.split()[-1])
            x += val
    for row in crt:
        print(''.join(row))

with open('../data/10.txt', 'r') as f:
    instructions = [line.strip() for line in f.readlines()]
    print(part1(instructions))
    part2(instructions)
