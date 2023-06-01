from unidecode import unidecode

from base import MetricBase

class MetricKarmicDebt(MetricBase):
    def __init__(self, full_name: str):
        self.full_name = unidecode(full_name).lower().strip()

    def calculate(self):
        number_list = [1,2,3,4,5,6,7,8,9]
        group_words = self.full_name.split(" ")

        for word in group_words:
            for letter in word:
                num = self.ALPHABET_NUMBER.get(letter)
                if num in number_list:
                    number_list.remove(num)
        return number_list

    def count_repeated_number(self):
        group_words = self.full_name.replace(" ", "")
        group_numbers = []

        for letter in group_words:
            group_numbers.append(self.ALPHABET_NUMBER.get(letter))

        max_numbers = []
        max_count = 0
        for number in group_numbers:
            number_count = group_numbers.count(number)
            if number_count > max_count:
                max_count = number_count
        for number in group_numbers:
            number_count = group_numbers.count(number)
            if number_count == max_count and number not in max_numbers:
                max_numbers.append(number)
        return max_numbers


