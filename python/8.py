def process_line(line):
    return [int(c) for c in line[:-1]]

def count_visible(grid):
    result = 0
    r, c = len(grid), len(grid[0])
    result += 2*c + 2*(r-2) # boundary trees

    seen = set()

    for ri in range(1, r-1):
        # go right
        max_so_far = grid[ri][0]
        for cj in range(1, c-1, 1):
            if grid[ri][cj] > max_so_far:
                if (ri, cj) not in seen:
                    result += 1
                    seen.add((ri, cj))
                max_so_far = grid[ri][cj]

        # go left
        max_so_far = grid[ri][c-1]
        for cj in range(c-2, 0, -1):
            if grid[ri][cj] > max_so_far:
                if (ri, cj) not in seen:
                    result += 1
                    seen.add((ri, cj))
                max_so_far = grid[ri][cj]

    for ci in range(1, c-1):
        # go down
        max_so_far = grid[0][ci]
        for rj in range(1, r-1, 1):
            if grid[rj][ci] > max_so_far:
                if (rj, ci) not in seen:
                    result += 1
                    seen.add((rj, ci))
                max_so_far = grid[rj][ci]

        # go up
        max_so_far = grid[r-1][ci]
        for rj in range(r-2, 0, -1):
            if grid[rj][ci] > max_so_far:
                if (rj, ci) not in seen:
                    result += 1
                    seen.add((rj, ci))
                max_so_far = grid[rj][ci]

    return result

def best_score(grid):
    r, c = len(grid), len(grid[0])
    result = 1

    # ignore the outermost trees, they'll always have a scenic score of 0
    for ri in range(1, r-1):
        for cj in range(1, c-1):
            # go up
            up = 0
            for rk in range(ri-1, -1, -1):
                up += 1
                if grid[rk][cj] >= grid[ri][cj]:
                    break

            # go down
            down = 0
            for rk in range(ri+1, r):
                down += 1
                if grid[rk][cj] >= grid[ri][cj]:
                    break

            # go left
            left = 0
            for ck in range(cj-1, -1, -1):
                left += 1
                if grid[ri][ck] >= grid[ri][cj]:
                    break

            # go right
            right = 0
            for ck in range(cj+1, c):
                right += 1
                if grid[ri][ck] >= grid[ri][cj]:
                    break

            score = up * down * left * right
            result = max(score, result)

    return result

with open('8.txt', 'r') as f:
    grid = [process_line(line) for line in f.readlines()]
    print(count_visible(grid))
    print(best_score(grid))
