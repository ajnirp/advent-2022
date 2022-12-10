def adjacent(h, t):
    horz = h[0] == t[0] and abs(h[1] - t[1]) <= 1
    vert = h[1] == t[1] and abs(h[0] - t[0]) <= 1
    diag = abs(h[0] - t[0]) == 1 and abs(h[1] - t[1]) == 1
    return horz or vert or diag

def nbrs(pos):
    return [[pos[0]+dx, pos[1]+dy] for dx in [-1, 0, 1] for dy in [-1, 0, 1]]

def manhattan(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1-x2) + abs(y1-y2)

# return follower new position. follower tries to minimize Manhattan distance
# while making at most one step
def follow(follower_prev, leader_curr):
    if adjacent(follower_prev, leader_curr):
        return

    best = None
    best_dist = manhattan(follower_prev, leader_curr)
    for nbr in nbrs(follower_prev):
        dist = manhattan(nbr, leader_curr)
        if dist < best_dist:
            best_dist = dist
            best = nbr
    follower_prev[0] = best[0]
    follower_prev[1] = best[1]

def move_independent(direction, pos):
    if direction == 'R':
        pos[0] += 1
    elif direction == 'L':
        pos[0] -= 1
    elif direction == 'U':
        pos[1] += 1
    else:
        pos[1] -= 1

def single_move(direction, state):
    # move the head knot
    move_independent(direction, state[0])
    num_knots = len(state)
    for i in range(1, num_knots):
        # the other knots follow their immediate leader
        follow(state[i], state[i-1])

def process_move(direction, num, state, seen):
    for _ in range(num):
        single_move(direction, state)
        seen.add((state[-1][0], state[-1][1])) # update where the tail has been

def solve(moves, num_knots):
    state = [[0, 0] for _ in range(num_knots)]
    seen = set()
    for move in moves:
        direction, num = move.split()
        num = int(num)
        process_move(direction, num, state, seen)
    return len(seen)

with open('../data/9.txt', 'r') as f:
    moves = [line.strip() for line in f.readlines()]
    print(solve(moves, 2))
    print(solve(moves, 10))
