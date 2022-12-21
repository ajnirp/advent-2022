#!/snap/bin/pypy3
from copy import deepcopy

file = open('../data/17.txt')
gas = file.read().strip()
file.close()
fallen = 0
rocks = set()
brick_idx = 0 # 0 horizontal 1 cross 2 flipped L 3 vertical 4 square
gas_idx = 0
height = 0
prev_brick_idx = None
brick = []
while True:
    if brick_idx != prev_brick_idx:
        if brick_idx == 0:
            brick = [(2+x, height+3) for x in range(4)]
        elif brick_idx == 1:
            brick = [(2, height+4), (3, height+4), (4, height+4), (3, height+5), (3, height+3)]
        elif brick_idx == 2:
            brick = [(2, height+3), (3, height+3), (4, height+3), (4, height+4), (4, height+5)]
        elif brick_idx == 3:
            brick = [(2, height+3+y) for y in range(4)]
        elif brick_idx == 4:
            brick = [(2, height+3), (3, height+3), (2, height+4), (3, height+4)]
    if gas[gas_idx] == '>':
        new_pos = [(x+1,y) for x,y in brick]
        do_move = True
        for x,y in new_pos:
            if (x,y) in rocks or x > 6:
                do_move = False
                break
        if do_move:
            brick = [(x,y) for x,y in new_pos]
    elif gas[gas_idx] == '<':
        new_pos = [(x-1,y) for x,y in brick]
        do_move = True
        for x,y in new_pos:
            if (x,y) in rocks or x < 0:
                do_move = False
                break
        if do_move:
            brick = [(x,y) for x,y in new_pos]
    new_pos = [(x,y-1) for x,y in brick]
    do_move = True
    for x,y in new_pos:
        if (x,y) in rocks or y < 0:
            do_move = False
            break
    prev_brick_idx = brick_idx
    if do_move:
        brick = [(x,y) for x,y in new_pos]
    else:
        for x,y in brick:
            rocks.add((x,y))
        fallen += 1
        brick_idx = (brick_idx+1)%5
        height = max(height, max(1+y for _,y in brick))

        # for the fallen brick, check if we can close a row for any of its y
        # coords
        closed = []
        for _,y in brick:
            if all((x,y) in rocks for x in range(7)):
                closed.append(y)
        if closed:
            closed = max(closed)
            rocks = set((x,y) for x,y in rocks if y >= closed)

        # if brick_idx not in [1,2]:
        #     max_y = max(y for _,y in brick)
        #     if height == 1+max_y and all((x, max_y) in rocks for x in range(7)):
        #         print('woo', fallen, height)
    gas_idx = (gas_idx+1)%len(gas)
    if fallen % 10000 == 0:
        print(len(rocks))
    if fallen == int(1e6):
        print(height)
        break

# for y in range(height-1,-1,-1):
#     for x in range(7):
#         if (x,y) in rocks:
#             print('#', end='')
#         else:
#             print('.', end='')
#     print()