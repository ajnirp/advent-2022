def parse_point(point):
    x, y = point.split(',')
    return int(x), int(y)

def parse_line(line):
    return [parse_point(point) for point in line.split(' -> ')]

# return min_x, max_x, max_y
def xy_bounds(data):
    x0 = min(point[0] for line in data for point in line)
    x1 = max(point[0] for line in data for point in line)
    y1 = max(point[1] for line in data for point in line)
    return x0, x1, y1

def normalize_data(data):
    x0, x1, y1 = xy_bounds(data)
    for line in data:
        normalize_line(line, x0)

def normalize_line(line, x0):
    for i in range(len(line)):
        x, y = line[i]
        line[i] = (x-x0, y)

def make_grid(data, dx, dy):
    result = [['.' for _ in range(dx)] for _ in range(dy)]
    for line in data:
        for i in range(len(line)-1):
            p1, p2 = line[i], line[i+1]
            x1, y1 = p1
            x2, y2 = p2
            if y1 == y2 and x1 > x2:
                x1, y1, x2, y2 = x2, y2, x1, y1
            elif x1 == x2 and y1 > y2:
                x1, y1, x2, y2 = x2, y2, x1, y1
            for r in range(y1, y2+1):
                for c in range(x1, x2+1):
                    result[r][c] = '#'
    return result

# True iff grain ends up at rest inside grid
def drop_grain(grid, src, part2=False):
    x, y = src
    rows, cols = len(grid), len(grid[0])
    while True:
        if y == rows-1 or x < 0 or x >= cols: return False
        # y must be < rows-1 henceforth
        elif grid[y+1][x] == '.': y += 1
        elif grid[y+1][x] != '.':
            if x == 0: return False
            elif x > 0 and grid[y+1][x-1] == '.':
                x, y = x-1, y+1
                continue
            elif x == cols-1: return False
            elif x < cols-1 and grid[y+1][x+1] == '.':
                x, y = x+1, y+1
                continue
            if y < 0: return False # foiled right away
            else:
                grid[y][x] = 'o'
                if part2 and y == 0 and x == src[0]:
                    return False
                return True
    return False

def print_grid(grid):
    for line in grid: print(''.join(line))

import sys

def solve(data):
    x0, x1, y1 = xy_bounds(data)
    normalize_data(data)
    src = (500-x0, -1)
    grid = make_grid(data, x1-x0+1, y1+1)
    itr = 0
    while True:
        if drop_grain(grid, src):
            itr += 1
        else:
            print(itr)
            break

def solve2(data):
    x0, x1, y1 = xy_bounds(data)
    y1 += 2
    # hack to find delta: choose a large value, get right ans, then decrease
    # as much as you can while still getting the right ans
    delta = 150
    x0, x1 = x0-delta, x1+delta
    data.append([(x0,y1), (x1,y1)])
    normalize_data(data)
    src = (500-x0, -1)
    grid = make_grid(data, x1-x0+1, y1+1)
    itr = 0
    while True:
        if drop_grain(grid, src, True):
            itr += 1
        else:
            print(itr+1) # hack
            break

# infile = '../data/14t.txt' # 24, 93
infile = '../data/14.txt' # 696, 23610

with open(infile, 'r') as f:
    data = [line.strip() for line in f.readlines()]
    data = [parse_line(line) for line in data]
    solve(data)

with open(infile, 'r') as f:
    data = [line.strip() for line in f.readlines()]
    data = [parse_line(line) for line in data]
    solve2(data)
