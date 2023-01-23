#!/usr/bin/python3
#./22.py < ../data/22.txt

DX = [1,0,-1,0]
DY = [0,1,0,-1]

# input: '10R5L5R10L4R5L5'
# output: [10, 'R', 5, 'L', 5, 'R', ..., 'L', 5]
def parse_instructions(instructions):
    buffer, result = [], []
    for char in instructions:
        if char.isdigit():
            buffer.append(char)
        else:
            result.extend([int(''.join(buffer)), char])
            buffer.clear()
    result.append(int(''.join(buffer)))
    return result
# assert(parse_instructions('10R2L3R10L4R7L5') == [10,'R',2,'L',3,'R',10,'L',4,'R',7,'L',5])

with open(0) as file:
    data = file.readlines()

# [:-1] to remove newline at the end
grid = [line[:-1] for line in data[:200]]
instructions = parse_instructions(data[-1])
# assert(instructions[-1] == 41)

X = max(map(len, grid))
Y = len(grid)
# assert(X == 150 and Y == 200)

for ri in range(len(grid)):
    grid[ri] = grid[ri].ljust(X, ' ')
# assert(all(len(row) == X for row in grid))


leftmost, rightmost = [], []
for row_idx in range(Y):
    for col_idx in range(X):
        if grid[row_idx][col_idx] in '.#':
            leftmost.append(col_idx)
            break
    for col_idx in range(X-1,-1,-1):
        if grid[row_idx][col_idx] in '.#':
            rightmost.append(col_idx)
            break
# assert(leftmost == [50]*100 + [0]*100)
# assert(rightmost == [149]*50 + [99]*100 + [49]*50)

topmost, bottommost = [], []
for col_idx in range(X):
    for row_idx in range(Y):
        if grid[row_idx][col_idx] in '.#':
            topmost.append(row_idx)
            break
    for row_idx in range(Y-1,-1,-1):
        if grid[row_idx][col_idx] in '.#':
            bottommost.append(row_idx)
            break
# assert(topmost == [100]*50 + [0]*100)
# assert(bottommost == [199]*50 + [149]*50 + [49]*50)

def execute_instruction(instruction, grid, pos, heading):
    dy, dx = DY[heading], DX[heading]
    y, x = pos
    for step in range(instruction):
        ny, nx = (y+dy)%Y, (x+dx)%X
        if grid[ny][nx] not in '.#':
            if heading == 0: nx = leftmost[ny]
            elif heading == 1: ny = topmost[nx]
            elif heading == 2: nx = rightmost[ny]
            elif heading == 3: ny = bottommost[nx]
        if grid[ny][nx] == '.':
            y, x = ny, nx
        elif grid[ny][nx] == '#':
            return (y, x), heading
    return (y, x), heading

# heading: 0 right 1 down 2 left 3 up
def execute_instructions(instructions, grid, pos, heading):
    for instruction in instructions:
        if instruction == 'L':
            heading = (heading-1)%4
        elif instruction == 'R':
            heading = (heading+1)%4
        else:
            pos, heading = execute_instruction(instruction, grid, pos, heading)
    y, x = pos
    return 1000*(y+1) + 4*(x+1) + heading

print(execute_instructions(instructions, grid, (0, leftmost[0]), 0)) # 136054
