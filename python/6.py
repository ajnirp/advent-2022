def find_first_index(data, n):
    for i in range(n, len(data)):
        substr = data[i-n+1:i+1]
        if len(set(substr)) == n:
            return i+1

with open('../data/6.txt', 'r') as f:
    data = f.read().strip()
    print(find_first_index(data, 4))
    print(find_first_index(data, 14))
