from typing import List
from datetime import datetime

from base import MetricBase

DATA = {
    "chi_so_thai_do": {
        "special_value": {11: "11/2", 22: "22/4"}
    },
    "nam_ca_nhan": {
        "special_value": {11: "11/2", 22: "22/4"}
    },
    "chi_so_duong_doi": {
        "special_value": {11: "11/2", 22: "22/4", 13: "13/4", 14: "14/5", 16: "16/7", 19: "19/1"}
    },
    "chi_so_ngay_sinh": {
        "special_value": {11: "11/2", 22: "22/4", 13: "13/4", 14: "14/5", 16: "16/7", 19: "19/1"}
    },
    "bieu_do_duong_doi":{
        "special_value": {11: "11/2", 22: "22/4"}
    }
}


class MetricBirthday(MetricBase):

    def __init__(self, birthday: str):
        self.day, self.month, self.year = self.from_date_string(birthday)

    @staticmethod
    def from_date_string(date_string: str):
        format_ddmmyyyy = "%d-%m-%Y"  # 20-12-1993
        try:
            date = datetime.strptime(date_string, format_ddmmyyyy)
        except ValueError:
            raise ValueError("Lỗi: Không đúng định dạng ngày tháng năm sinh!")

        return date.day, date.month, date.year

    def calculate(self, metric_type: str) -> str:
        special_value = DATA.get(metric_type, {}).get("special_value", {})
        day = self.convert_to_single_number([self.day], special_value)
        month = self.convert_to_single_number([self.month], special_value)

        final_numbers = self.convert_to_single_number([day, month], special_value)
        if metric_type == "nam_ca_nhan":
            now = datetime.now()
            year = self.convert_to_single_number([now.year], special_value)
            final_numbers = self.convert_to_single_number([day, month, year], special_value)
        if metric_type == "chi_so_duong_doi":
            year = self.convert_to_single_number([self.year], special_value)
            final_numbers = self.convert_to_single_number([day, month, year], special_value)
        if metric_type == "chi_so_ngay_sinh":
            final_numbers = self.convert_to_single_number([day], special_value)
        if final_numbers in list(special_value.keys()):
            return special_value.get(final_numbers)
        else:
            return str(final_numbers)

    def calculate_life_chart(self, metric_type: str) -> List[str]:
        special_value = DATA.get(metric_type, {}).get("special_value", {})
        day = self.convert_to_single_number([self.day], special_value)
        month = self.convert_to_single_number([self.month], special_value)
        year = self.convert_to_single_number_without_reduce([self.year], special_value)

        dinh_1 = self.convert_to_single_number([day, month], special_value)
        dinh_2 = self.convert_to_single_number([day, year], special_value)
        dinh_3 = self.convert_to_single_number([dinh_1, dinh_2], special_value)
        dinh_4 = self.convert_to_single_number([month, year], special_value)

        tmp = [day, month, year, dinh_1, dinh_2, dinh_3, dinh_4]
        result = []

        for item in tmp:
            if item in special_value.keys():
                item = special_value.get(item)
            result.append(str(item))
        return result

    def count_birth_day(self):
        date_list = []
        for item in str(self.day):
            if item != "0":
                date_list.append(int(item))

        for item in str(self.month):
            if item != "0":
                date_list.append(int(item))

        for item in str(self.year):
            if item != "0":
                date_list.append(int(item))
        raw = {i: date_list.count(i) for i in date_list}
        if None in raw:
            del raw[None]
        return {key: val for key, val in sorted(raw.items(), key = lambda ele: ele[0])}

    def calculate_age(self):
        return datetime.now().year - self.year
