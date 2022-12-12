from collections import deque

class Grid:
    def __init__(self, data):
        self.grid = [[e for e in row] for row in data]
        self.r = len(self.grid)
        self.c = len(self.grid[0])
        self.start = self.end = None
        self.starts = []
        # while finding start and end, overwrite those positions with 'a' and
        # 'z' respectively
        for r in range(self.r):
            for c in range(self.c):
                if self.grid[r][c] == 'S' and not self.start:
                    self.start = (r, c)
                    self.grid[r][c] = 'a'
                elif self.grid[r][c] == 'E' and not self.end:
                    self.end = (r, c)
                    self.grid[r][c] = 'z'
                elif self.grid[r][c] == 'a':
                    self.starts.append((r, c))

    def contains(self, pos):
        r, c = pos
        return 0 <= r < self.r and 0 <= c < self.c

    def can_step(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        return ord(self.grid[r2][c2]) <= ord(self.grid[r1][c1]) + 1

    def nbrs(self, pos):
        r, c = pos
        candidates = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
        return [cand for cand in candidates if self.contains(cand) and self.can_step(pos, cand)]

    def search(self, start):
        q = deque([(start, 0)])
        seen = set([start])
        while q:
            curr, dist = q.popleft()
            if curr == self.end:
                return dist
            for nbr in self.nbrs(curr):
                if nbr not in seen:
                    seen.add(nbr)
                    q.append((nbr, dist+1))
        return 1e10

    def shortest(self):
        return min(map(self.search, self.starts))

with open('../data/12.txt', 'r') as f:
    data = [line.strip() for line in f.readlines()]
    grid = Grid(data)
    print(grid.search(grid.start))
    print(grid.shortest())
