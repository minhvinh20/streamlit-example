from typing import List

def count_repeated_number(numbers: List[int]):
    max_numbers = []
    max_count = 0
    for number in numbers:
        number_count = numbers.count(number)
        if number_count > max_count:
            max_count = number_count
    for number in numbers:
        number_count = numbers.count(number)
        if number_count == max_count and number not in max_numbers:
            max_numbers.append(number)
    if len(max_numbers) == len(numbers):
        return None
    return max_numbers