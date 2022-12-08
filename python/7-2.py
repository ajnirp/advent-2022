from collections import defaultdict

CUTOFF = 100_000
TOTAL_SPACE = 70_000_000
UNUSED_REQUIRED = 30_000_000

# Skip dir lines. Skip ls lines. Store every dir size in a map. When you see a
# file, update size for its parent dir as well as each ancestor.
with open('7.txt', 'r') as f:
    cwd = []
    sizes = defaultdict(int)
    for line in f.readlines():
        line = line.strip()
        if line[:3] == 'dir':
            continue
        elif line[2] == 'l':
            continue
        elif line[0] == '$':
            dst = line.split()[-1]
            if dst == '/':
                cwd = []
            elif dst == '..':
                cwd.pop()
            else:
                cwd.append(dst)
        elif line[0] in '123456789':
            size, file = line.split()
            size = int(size)
            dir_path = '/'.join(cwd)
            sizes[dir_path] += size
            cwd_copy = [d for d in cwd]
            while cwd_copy:
                cwd_copy.pop()
                parent = '/'.join(cwd_copy)
                sizes[parent] += size
    print(sum(v for v in sizes.values() if v < CUTOFF))
    total_used = sizes['']
    space_to_free = UNUSED_REQUIRED + total_used - TOTAL_SPACE
    smallest_size = total_used
    for v in sizes.values():
        if v > space_to_free:
            smallest_size = min(smallest_size, v)
    print(smallest_size)
