from typing import List, Dict

class MetricBase:
    ALPHABET_NUMBER = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "f": 6,
        "g": 7,
        "h": 8,
        "i": 9,
        "j": 1,
        "k": 2,
        "l": 3,
        "m": 4,
        "n": 5,
        "o": 6,
        "p": 7,
        "q": 8,
        "r": 9,
        "s": 1,
        "t": 2,
        "u": 3,
        "v": 4,
        "w": 5,
        "x": 6,
        "y": 7,
        "z": 8,
    }
    DATA = {
        "chi_so_truong_thanh": {
            "special_value": {11: "11/2", 22: "22/4"}
        },
    }
    def convert_to_single_number(self, lst_numbers: List[int], special_value: Dict[int, str]):
        total = 0
        special = 0
        for number in lst_numbers:
            if number in special_value.keys():
                special = number
            total += number
            if total in special_value.keys():
                special = total

        if special != 0 and (total - special) % 9 == 0:
            return special

        if total in special_value.keys():
            return total
        return total % 9 if total % 9 != 0 else 9


    def convert_to_single_number_without_reduce(self, lst_numbers: List[int], special_value: Dict[int, str]):
        total = sum(lst_numbers)
        if total > 9 and total not in list(special_value.keys()):
            return self.convert_to_single_number_without_reduce(
                lst_numbers=[int(x) for x in str(total)],
                special_value=special_value
            )
        return total
