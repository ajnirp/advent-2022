#!/snap/bin/pypy3

from collections import deque

def parse_cube(line):
	a, b, c = map(int, line.strip().split(','))
	return a, b, c
	
def nbrs(cube):
	deltas = [
		(-1, 0, 0), (1, 0, 0),
		(0, -1, 0), (0, 1, 0),
		(0, 0, -1), (0, 0, 1),
	]
	x, y, z = cube
	for dx, dy, dz in deltas:
		yield (x+dx, y+dy, z+dz)
		
def unexposed_sides(cube, cubes):
	return sum(nbr not in cubes for nbr in nbrs(cube))
	
def bounding_box(cubes):
	minx = min(cube[0] for cube in cubes)
	miny = min(cube[1] for cube in cubes)
	minz = min(cube[2] for cube in cubes)
	maxx = max(cube[0] for cube in cubes)
	maxy = max(cube[1] for cube in cubes)
	maxz = max(cube[2] for cube in cubes)
	return (minx, miny, minz), (maxx, maxy, maxz)

# Starting from an air block, explore air blocks until you either
# reach the outside (in which case you found no trapped air) or
# you exhaust the queue (in which case everything you encountered
# was trapped air)
def explore(position, cubes):
	queue = deque([position])
	trapped_air = set([position])
	(minx, miny, minz), (maxx, maxy, maxz) = bounding_box(cubes)
	while queue:
		curr = queue.popleft()
		for nbr in nbrs(curr):
			if nbr in cubes or nbr in trapped_air: continue
			nx, ny, nz = nbr
			if not (minx <= nx <= maxx): return set()
			if not (miny <= ny <= maxy): return set()
			if not (minz <= nz <= maxz): return set()
			trapped_air.add(nbr)
			queue.append(nbr)
	return trapped_air

with open('../data/18.txt', 'r') as file:
	cubes = set(map(parse_cube, file.readlines()))

# Part 1
print(sum(unexposed_sides(cube, cubes) for cube in cubes))

(minx, miny, minz), (maxx, maxy, maxz) = bounding_box(cubes)
trapped_air = set()
for x in range(minx, maxx+1):
	for y in range(miny, maxy+1):
		for z in range(minz, maxz+1):
			position = (x, y, z)
			if position in cubes or position in trapped_air: continue
			trapped_air = trapped_air.union(explore(position, cubes))

# Count cube faces that aren't facing another cube and aren't facing trapped air		
def exterior_exposed_sides(cubes, trapped_air):
	(minx, miny, minz), (maxx, maxy, maxz) = bounding_box(cubes)
	result = 0
	for cube in cubes:
		for nbr in nbrs(cube):
			nx, ny, nz = nbr
			if not (minx <= nx <= maxx): result += 1; continue
			if not (miny <= ny <= maxy): result += 1; continue
			if not (minz <= nz <= maxz): result += 1; continue
			if nbr not in cubes and nbr not in trapped_air: result += 1
	return result

# Part 2
print(exterior_exposed_sides(cubes, trapped_air))
