user = input('ввести числа через запятую; ')
print('user:')
print(user)

numbers = user.split(',')
print('numbers:')
print(numbers)

for number in numbers:
    number = number.strip()
    integer = int(number)
    integer = integer ** 2
    print('результат:')
    print(integer)

print('конец')
