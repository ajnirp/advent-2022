with open('../data/1.txt', 'r') as f:
    data = f.read()

elves = data.strip().split('\n\n')
elves = [sum(map(int, elf.split('\n'))) for elf in elves] # total for each elf
elves.sort()
print(elves[-1]) # highest value
print(elves[-1] + elves[-2] + elves[-3]) # sum of top 3 values