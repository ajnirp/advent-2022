#!/usr/bin/python3
# ./25.py < ../data/25.txt

with open(0) as file:
	data = [line.strip() for line in file.readlines()]

def from_snafu(snafu):
	decimal = 0
	for char in snafu:
		digit = '=-012'.index(char) - 2
		decimal = decimal*5 + digit
	return decimal

def from_base_5(string):
	decimal = 0
	for char in string:
		decimal = decimal*5 + int(char)
	return decimal
	
def to_base_5(decimal):
	if decimal == 0:
		return '0'
	digits = []
	while decimal > 0:
		digits.append(str(decimal % 5))
		decimal //= 5
	return ''.join(reversed(digits))
	
# converts a base 5 string to snafu
# decreases value by '2' * len(string) in base 5
def base_5_to_snafu(string):
	return ['=-012'[int(char)] for char in string]

def to_snafu(decimal):
	base_5 = to_base_5(decimal)
	offset = from_base_5('2' * len(base_5))
	base_5_increased = to_base_5(decimal + offset)
	return ''.join(base_5_to_snafu(base_5_increased))

print(to_snafu(sum(from_snafu(string) for string in data)))
