#!/usr/bin/python3
# ./25.py < ../data/25.txt

def snafu_to_decimal(snafu):
	decimal = 0
	for char in snafu:
		digit = '=-012'.index(char) - 2
		decimal = decimal*5 + digit
	return decimal
	
def decimal_to_base_5(decimal):
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

def decimal_to_snafu(decimal):
	base_5 = decimal_to_base_5(decimal)
	offset = int('2' * len(base_5), 5)
	base_5_increased = decimal_to_base_5(decimal + offset)
	return ''.join(base_5_to_snafu(base_5_increased))

with open(0) as file:
	data = map(lambda line: line.strip(), file.readlines())
	print(decimal_to_snafu(sum(map(snafu_to_decimal, data))))
