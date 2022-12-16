#!/snap/bin/pypy3
# <14 seconds for execution
# solution to 2nd part taken from @jonathanpaulson after giving up
import sys
if len(sys.argv) != 3: sys.exit(1)
file = sys.argv[1]
y = int(sys.argv[2])

def coords(s):
    split = s.strip().split(', y=')
    return int(split[0][len('x='):]), int(split[1])

def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2)+abs(y1-y2)

f = open(file, 'r')
data = [line.strip() for line in f.readlines()]
S, B = [], set()
for line in data:
    line = line[len('Sensor at '):]
    colon = line.index(':')
    sx, sy = coords(line[:colon])
    b = coords(line[colon:][len(' closest beacon is at '):])
    B.add(b)
    S.append((sx, sy, dist((sx, sy), b)))

y = int(2e6)
result = sum((x,y) not in B and \
              not all(dist((x,y),(sx,sy)) > d \
              for sx,sy,d in S) \
              for x in range(-int(1e7), int(1e7)))
print(result)

# The missing beacon is outside the intersection of a bunch of diamond shapes.
# Since there is only one missing beacon, it must be at distance d+1 from a
# sensor, where d is that sensor's distance to its closest beacon. If it were
# larger than d+2, there would be another missing beacon adjacent to it because
# of the way that diamond shape intersections work.
for sx, sy, d in S:
    for dx in range(d+2):
        dy = d+1-dx
        for signx, signy in [(-1,1),(1,1),(1,-1),(-1,-1)]:
            x,y = sx+dx*signx, sy+dy*signy
            if not (0<=x<=int(4e6) and 0<=y<=int(4e6)): continue
            if all(dist((x,y),(ssx,ssy)) > dd for ssx,ssy,dd in S):
                print(x*int(4e6)+y)
                f.close()
                sys.exit(0)