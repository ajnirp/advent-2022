from copy import deepcopy

NUM_MONKEYS = 7

# # https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Using_the_existence_construction
# def bezout(a, n):
#     def extended_euclidean(a, b):
#         r0, r1 = a, b
#         s0, s1 = 1, 0
#         t0, t1 = 0, 1
#         while r1 != 0:
#             q = r0 // r1
#             r2 = r0 - q*r1
#             s2 = s0 - q*s1
#             t2 = t0 - q*t1
#             r0, r1 = r1, r2
#             s0, s1 = s1, s2
#             t0, t1 = t1, t2
#         return s0, t0
#     for i in range(len(n)-1):
#         a1, a2 = a[i:i+2]
#         n1, n2 = n[i:i+2]
#         m1, m2 = extended_euclidean(n1, n2)
#         n[i+1] = n1*n2
#         a[i+1] = (a1*m2*n2 + a2*m1*n1) % (n1*n2)
#     return a[-1]

class Monkey:
    def __init__(self, items, operation, divisible, throw_to):
        self.items = items
        self.operation = operation
        self.operation = operation
        self.divisible = divisible
        self.divisible = divisible
        self.throw_to = throw_to

    def clear_items(self):
        self.items.clear()

    def add_item(self, item):
        self.items.append(item)

def parse_data(data):
    return [parse_monkey(monkey) for monkey in data.split('\n\n')]

def parse_monkey(data):
    lines = [line.strip() for line in data.split('\n')]
    items = [int(i) for i in lines[1][len('Starting items: '):].split(', ')]
    operation = lines[2][len('Operation: new = '):].replace('old', 'x')
    operation = eval('lambda x: ' + operation)
    divisible = int(lines[3].split()[-1])
    throw_to = (int(lines[4].split()[-1]), int(lines[5].split()[-1]))    
    return Monkey(items, operation, divisible, throw_to)

class State:
    def __init__(self, monkeys, worry_decreases=True):
        self.monkeys = deepcopy(monkeys) # don't mutate the input
        self.num_inspections = [0 for _ in range(len(self.monkeys))]
        self.worry_decreases = worry_decreases

    def normalize_worry(self, worry):
        # they're all prime, so find worry modulo their product
        return worry % 9699690
        # a = [worry % monkey.divisible for monkey in self.monkeys]
        # n = [monkey.divisible for monkey in self.monkeys]
        # if all(e == 0 for e in a):
        #     return 0
        # return bezout(a, n)

    def do_rounds(self, n):
        for i in range(n):
            for i in range(len(self.monkeys)):
                self.do_monkey(i)

    def do_monkey(self, i):
        monkey = self.monkeys[i]
        for item in monkey.items:
            worry = monkey.operation(item)
            if self.worry_decreases:
                worry //= 3
            target = monkey.throw_to[1] # most likely goes to 'not'
            if worry % monkey.divisible == 0:
                target = monkey.throw_to[0]
            worry = self.normalize_worry(worry)
            self.monkeys[target].add_item(worry)
        self.num_inspections[i] += len(monkey.items)
        self.monkeys[i].clear_items()

    def monkey_business(self, n):
        self.do_rounds(n)
        self.num_inspections.sort()
        return self.num_inspections[-1] * self.num_inspections[-2]

with open('../data/11.txt', 'r') as f:
    data = f.read().strip()
    monkeys = parse_data(data)
    state = State(monkeys, True)
    print(state.monkey_business(20))
    state = State(monkeys, False)
    print(state.monkey_business(10000))