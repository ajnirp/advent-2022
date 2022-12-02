first_col_map = {
    'A': 'R',
    'B': 'P',
    'C': 'S'
}

second_col_map = {
    'X': 'R',
    'Y': 'P',
    'Z': 'S'
}

val = {
    'R': 1,
    'P': 2,
    'S': 3,
}

defeater = {
    'R': 'S',
    'S': 'P',
    'P': 'R',
}

defeated_by = {v: k for k, v in defeater.items()}

with open('2.txt', 'r') as f:
    score = 0
    score_2 = 0
    data = f.readlines()
    for line in data:
        a, b = line[0], line[-2]

        them = first_col_map[a]
        me = second_col_map[b]

        score += val[me]
        if me == them:
            score += 3
        elif defeater[me] == them:
            score += 6

        if b == 'Y':
            score_2 += 3 + val[them]
        elif b == 'X':
            score_2 += val[defeater[them]]
        else:
            score_2 += 6 + val[defeated_by[them]]

print(score, score_2)
