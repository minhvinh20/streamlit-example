from unidecode import unidecode

from base import MetricBase

DATA = {
    "chi_so_noi_tam": {
        "words": ["a", "e", "i", "o", "u"],
        "special_value": {11: "11/2", 22: "22/4", 13: "13/4", 14: "14/5", 16: "16/7", 19: "19/1"}
    },
    "chi_so_logic": {
        "words": ["a", "g", "h", "j", "l", "n", "p"],
        "special_value": {11: "11/2", 22: "22/4"}
    },
    "chi_so_cam_xuc": {
        "words": ["b", "i", "o", "r", "s", "t", "x", "z"],
        "special_value": {11: "11/2", 22: "22/4"}
    },
    "chi_so_truc_giac": {
        "words": ["c", "f", "k", "q", "u", "v", "y"],
        "special_value": {11: "11/2", 22: "22/4"}
    },
    "chi_so_trai_nghiem": {
        "words": ["d", "e", "m", "w"],
        "special_value": {11: "11/2", 22: "22/4"}
    },
    "chi_so_tuong_tac": {
        "words": [
            "b",
            "c",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "l",
            "m",
            "n",
            "p",
            "q",
            "r",
            "s",
            "t",
            "v",
            "w",
            "x",
            "z",
        ],
        "special_value": {13: "13/4", 14: "14/5", 16: "16/7", 19: "19/1"}
    },
    "chi_so_su_menh": {
        "words": [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z"
        ],
        "special_value": {11: "11/2", 22: "22/4", 13: "13/4", 14: "14/5", 16: "16/7", 19: "19/1"}
    },
    "words": {}
}


class MetricFullName(MetricBase):

    def __init__(self, full_name: str):
        self.full_name = unidecode(full_name).lower().strip()

    def calculate(self, metric_type: str) -> str:
        so_vua = [11, 22]
        words = DATA.get(metric_type, {}).get("words", [])
        special_value = DATA.get(metric_type, {}).get("special_value", {})
        group_words = self.full_name.split(" ")

        total_numbers = []
        for group_word in group_words:
            numbers = []
            if metric_type == "chi_so_noi_tam":
                list_word = list(group_word)
                if "y" in list_word:
                    y_index = list_word.index("y")
                    prev = None
                    next = None
                    if y_index != 0:
                        prev = list_word[y_index - 1]
                    if y_index + 1 < len(list_word):
                        next = list_word[y_index + 1]
                    if prev and prev not in words and not next:
                        numbers.append(7)
                    elif prev and next and (prev not in words or next not in words):
                        numbers.append(7)

            if metric_type == "chi_so_tuong_tac":
                list_word = list(group_word)
                if "y" in list_word:
                    y_index = list_word.index("y")
                    prev = None
                    next = None
                    if y_index != 0:
                        prev = list_word[y_index - 1]
                    if y_index + 1 < len(list_word):
                        next = list_word[y_index + 1]
                    if prev and prev not in words and not next:
                        numbers.append(7)
                    elif prev and next and (prev not in words or next not in words):
                        numbers.append(7)

            if metric_type in ["chi_so_can_bang"]:
                numbers.append(self.ALPHABET_NUMBER.get(group_word[0]))

            for word in group_word:
                if word in words:
                    numbers.append(self.ALPHABET_NUMBER.get(word))

            # Validate list number
            if None in numbers:
                raise ValueError(f"Lỗi: Có một từ trong {words} không tìm thấy được giá trị số của nó!")

            if numbers and metric_type not in ["chi_so_su_menh", "chi_so_noi_tam", "chi_so_tuong_tac", "chi_so_cam_xuc"]:
                total_numbers.append(self.convert_to_single_number(numbers, special_value))
            elif metric_type in ["chi_so_su_menh", "chi_so_noi_tam", "chi_so_tuong_tac", "chi_so_cam_xuc"]:
                total_numbers.append(self.convert_to_single_number(numbers, {}))



        # nếu không tìm thấy giá trị của tất cả các từ
        # thì hàm trả về giá trị là 1
        if not total_numbers:
            return "1"

        final_numbers = self.convert_to_single_number(total_numbers, special_value)
        if (final_numbers in list(special_value.keys()) and final_numbers in so_vua) or final_numbers in list(special_value.keys()):
            return special_value.get(final_numbers)
        else:
            return str(final_numbers)

    def calculate_full_name_chart(self):
        number_list = []
        for char in self.full_name:
            number_list.append(self.ALPHABET_NUMBER.get(char))
        raw = {i: number_list.count(i) for i in number_list}
        if None in raw:
            del raw[None]
        return {key: val for key, val in sorted(raw.items(), key = lambda ele: ele[0])}

