
import shutil

import reportlab.lib.colors
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
import io

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from metric_full_name import MetricFullName
from metric_birthday import MetricBirthday
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel

from services.name_metrics import (
    ChiSoNoiTam,
    ChiSoLogic,
    ChiSoCamXuc,
    ChiSoTrucGiac,
    ChiSoTraiNghiem,
    ChiSoBaiHocNghiep,
    ChiSoTuongTac,
    ChiSoCanBang,
    ChiSoSuMenh,
    ChiSoDamMe,
)
from services.birthday_metrics import (
    ChiSoThaiDo,
    NamCaNhan,
    ChiSoDuongDoi,
    ChiSoNgaySinh,
    BieuDoDuongDoi,
)
from services.special_metrics import (
    ChiSoTruongThanh,
    ChiSoLap,
    ChiSoNoiTamVaTuongTac,
    ChiSoSuMenhVaDuongDoi,
    ChiSoNoNghiep,
)

a = [
    "chi_so_noi_tam",
    "chi_so_logic",
    "chi_so_cam_xuc",
    "chi_so_truc_giac",
    "chi_so_trai_nghiem",
    "chi_so_tuong_tac",
    "chi_so_su_menh",
]


def main():
    full_name = input("Nhập họ tên đầy đủ của bạn: ")
    birthday = input("Nhập ngày tháng năm sinh của bạn (vd: 28-10-1993): ")

    #full_name = "Dao Thi Hong Hai"
    #birthday = "16-06-1981"

    metric_full_name = MetricFullName(full_name)
    metric_birthday = MetricBirthday(birthday)

    chi_so_bai_hoc_nghiep = ChiSoBaiHocNghiep(full_name=full_name).calculate()

    chi_so_noi_tam = ChiSoNoiTam(full_name=full_name).calculate()
    chi_so_logic = ChiSoLogic(full_name=full_name).calculate()
    chi_so_cam_xuc = ChiSoCamXuc(full_name=full_name).calculate()
    chi_so_truc_giac = ChiSoTrucGiac(full_name=full_name).calculate()
    chi_so_trai_nghiem = ChiSoTraiNghiem(full_name=full_name).calculate()
    chi_so_tiem_thuc = 9 - len(chi_so_bai_hoc_nghiep.split(",") if chi_so_bai_hoc_nghiep else [])

    chi_so_thai_do = ChiSoThaiDo(birthday=birthday).calculate()
    chi_so_tuong_tac = ChiSoTuongTac(full_name=full_name).calculate()

    chi_so_can_bang = ChiSoCanBang(full_name=full_name).calculate()

    nam_ca_nhan = NamCaNhan(birthday=birthday).calculate()
    chi_so_su_menh = ChiSoSuMenh(full_name=full_name).calculate()
    chi_so_duong_doi = ChiSoDuongDoi(birthday=birthday).calculate()
    chi_so_ngay_sinh = ChiSoNgaySinh(birthday=birthday).calculate()

    chi_so_truong_thanh = ChiSoTruongThanh(chi_so_su_menh=chi_so_su_menh, chi_so_duong_doi=chi_so_duong_doi).calculate()

    chi_so_dam_me = ChiSoDamMe(full_name=full_name).calculate()

    chi_so_lap = ChiSoLap(chi_so_su_menh=chi_so_su_menh, chi_so_duong_doi=chi_so_duong_doi,
                          chi_so_ngay_sinh=chi_so_ngay_sinh, chi_so_noi_tam=chi_so_noi_tam,
                          chi_so_tuong_tac=chi_so_tuong_tac, chi_so_thai_do=chi_so_thai_do).calculate()

    chi_so_noi_tam_va_tuong_tac = ChiSoNoiTamVaTuongTac(chi_so_noi_tam=chi_so_noi_tam,
                                                        chi_so_tuong_tac=chi_so_tuong_tac).calculate()
    chi_so_su_menh_va_duong_doi = ChiSoSuMenhVaDuongDoi(chi_so_su_menh=chi_so_su_menh,
                                                        chi_so_duong_doi=chi_so_duong_doi).calculate()

    bieu_do_duong_doi = BieuDoDuongDoi(birthday=birthday).calculate()
    bieu_do_duong_doi = bieu_do_duong_doi.split(",")

    bieu_do_ngay_sinh = metric_birthday.count_birth_day()
    bieu_do_ho_ten = metric_full_name.calculate_full_name_chart()

    chi_so_no_nghiep = ChiSoNoNghiep(chi_so_su_menh=chi_so_su_menh, chi_so_duong_doi=chi_so_duong_doi,
                                     chi_so_noi_tam=chi_so_noi_tam, chi_so_tuong_tac=chi_so_tuong_tac,
                                     chi_so_ngay_sinh=chi_so_ngay_sinh, nam_ca_nhan=nam_ca_nhan,
                                     bieu_do_duong_doi_2=bieu_do_duong_doi[2], bieu_do_duong_doi_3=bieu_do_duong_doi[3],
                                     bieu_do_duong_doi_4=bieu_do_duong_doi[4], bieu_do_duong_doi_5=bieu_do_duong_doi[5],
                                     bieu_do_duong_doi_6=bieu_do_duong_doi[6]).calculate()

    customer_age = metric_birthday.calculate_age()

    print("*=====================================================================")
    print("                        THẤU HIỂU BẢN THÂN                            ")
    print("====================================================================*/")
    print("------------------------ Thế giới bên trong -------------------------")
    data = {
        "Chỉ số nội tâm": chi_so_noi_tam,
        "Chỉ số logic": chi_so_logic,
        "Chỉ số cảm xúc": chi_so_cam_xuc,
        "Chỉ số trực giác": chi_so_truc_giac,
        "Chỉ số trải nghiệm": chi_so_trai_nghiem,
        "Chỉ số tiềm thức": chi_so_tiem_thuc
    }
    result = [Panel(f"[b]{key}[/b]\n[yellow]{value}", expand=True) for key, value in data.items()]
    console = Console()
    console.print(Columns(result))

    print("------------------------ Thế giới bên ngoài -------------------------")
    data = {
        "Chỉ số lặp": chi_so_lap,
        "Chỉ số thái độ": chi_so_thai_do,
        "Chỉ số tương tác": chi_so_tuong_tac,
    }
    result = [Panel(f"[b]{key}[/b]\n[yellow]{value}", expand=True) for key, value in data.items()]
    console = Console()
    console.print(Columns(result))

    print("*=====================================================================")
    print("                       PHÁT TRIỂN BẢN THÂN                            ")
    print("====================================================================*/")
    data = {
        "Chỉ số cân bằng": chi_so_can_bang,
        "Chỉ số bài học nghiệp": chi_so_bai_hoc_nghiep,
        "Chỉ số nợ nghiệp": chi_so_no_nghiep
    }
    result = [Panel(f"[b]{key}[/b]\n[yellow]{value}", expand=True) for key, value in data.items()]
    console = Console()
    console.print(Columns(result))

    print("*=====================================================================")
    print("              ĐỊNH HƯỚNG SỰ NGHIỆP - MỤC ĐÍCH CUỘC ĐỜI                ")
    print("====================================================================*/")
    data = {
        "Năm cá nhân": nam_ca_nhan,
        "Chỉ số sứ mệnh": chi_so_su_menh,
        "Chỉ số đường đời": chi_so_duong_doi,
        "Chỉ số ngày sinh": chi_so_ngay_sinh,
        "Chỉ số trưởng thành": chi_so_truong_thanh,
        "Chỉ số đam mê": chi_so_dam_me,
    }
    result = [Panel(f"[b]{key}[/b]\n[yellow]{value}", expand=True) for key, value in data.items()]
    console = Console()
    console.print(Columns(result))

    print("*=====================================================================")
    print("                         NGUỒN LỰC HỖ TRỢ                             ")
    print("====================================================================*/")
    data = {
        "Chỉ số kết nối giữ Nội tâm và Tương tác": chi_so_noi_tam_va_tuong_tac,
        "Chỉ số kết nối giữ Sứ mệnh và Đường đời": chi_so_su_menh_va_duong_doi,
    }
    result = [Panel(f"[b]{key}[/b]\n[yellow]{value}", expand=True) for key, value in data.items()]
    console = Console()
    console.print(Columns(result))

    print("*=====================================================================")
    print("                      BIỂU ĐỒ CHẶNG ĐƯỜNG ĐỜI                         ")
    print("====================================================================*/")

    age_range = 36 - int(chi_so_duong_doi if "/" not in chi_so_duong_doi else chi_so_duong_doi.split("/")[0])
    if chi_so_duong_doi == '19/1':
        age_range = 36 - 1
    if chi_so_duong_doi == '22/4':
        age_range = 36 - 4
    if chi_so_duong_doi == '16/7':
        age_range = 36 - 7
    if chi_so_duong_doi == '14/5':
        age_range = 36 - 5
    if chi_so_duong_doi == '13/4':
        age_range = 36 - 4
    data = {
        "Ngày": bieu_do_duong_doi[0],
        "Tháng": bieu_do_duong_doi[1],
        "Năm": bieu_do_duong_doi[2],
        f"0 - {age_range}": bieu_do_duong_doi[3],
        f"{age_range + 1} - {age_range + 9}": bieu_do_duong_doi[4],
        f"{age_range + 10} - {age_range + 18}": bieu_do_duong_doi[5],
        f"{age_range + 19} - {age_range + 27}": bieu_do_duong_doi[6],
    }
    result = [Panel(f"[b]{key}[/b]\n[yellow]{value}", expand=True) for key, value in data.items()]
    console = Console()
    console.print(Columns(result))

    mapping_chang_duong_doi = {
        f"0 - {age_range}": bieu_do_duong_doi[3],
        f"{age_range + 1} - {age_range + 9}": bieu_do_duong_doi[4],
        f"{age_range + 10} - {age_range + 18}": bieu_do_duong_doi[5],
        f"{age_range + 19} - {age_range + 27}": bieu_do_duong_doi[6],
    }

    print("*=====================================================================")
    print("                           BIỂU ĐỒ Ikigai                             ")
    print("====================================================================*/")
    dam_me = []
    king_number = ["11/2", "24/4"]
    for item in chi_so_dam_me.split(","):
        item = str(item)
        if item in king_number:
            dam_me.append(item)
        else:
            dam_me.append(item.split("/")[1] if "/" in item else item)
    sn = [chi_so_duong_doi, chi_so_truong_thanh, nam_ca_nhan]
    # chang_duong_doi = None
    # for key in mapping_chang_duong_doi.keys():
    #     age = key.split(" - ")
    #     if customer_age >= int(age[0]) and customer_age <= int(age[1]):
    #         chang_duong_doi = mapping_chang_duong_doi.get(key)
    #         break
    # if chang_duong_doi:
    #     sn.append(chang_duong_doi)

    su_nghiep = []
    for item in sn:
        item = str(item)
        su_nghiep.append(item.split("/")[1] if "/" in item else item)
        # if item not in king_number:
        #     su_nghiep.append(item.split("/")[1] if "/" in item else item)
    su_nghiep = list(map(str, su_nghiep))

    cm = [chi_so_noi_tam, chi_so_tuong_tac, chi_so_ngay_sinh]
    chuyen_mon = []
    for item in cm:
        item = str(item)
        # if item in king_number:
        #     chuyen_mon.append(item)
        # else:
        #     chuyen_mon.append(item.split("/")[1] if "/" in item else item)
        chuyen_mon.append(item.split("/")[1] if "/" in item else item)
        # if item not in king_number:
        #     chuyen_mon.append(item.split("/")[1] if "/" in item else item)
        # else:
        #     chuyen_mon.append(item.split("/")[1] if "/" in item else item)
    special_items = []
    for item in chuyen_mon:
        if "/" in item:
            special_items.append(chuyen_mon.pop(chuyen_mon.index(item)))
    chuyen_mon = list(map(int, chuyen_mon))
    # chuyen_mon.sort() Bỏ sort chuyên môn
    chuyen_mon = list(map(str, chuyen_mon))
    if special_items:
        chuyen_mon = chuyen_mon + special_items

    data = {
        "Đam mê": ",".join(dam_me),
        "Sứ mệnh": chi_so_su_menh.split("/")[1] if "/" in chi_so_su_menh else chi_so_su_menh,
        "Chuyên môn": ",".join(map(str, chuyen_mon)),
        "Sự nghiệp": ",".join(su_nghiep),
    }
    result = [Panel(f"[b]{key}[/b]\n[yellow]{value}", expand=True) for key, value in data.items()]
    console = Console()
    console.print(Columns(result))

    print("*=====================================================================")
    print("                          BIỂU ĐỒ NGÀY SINH                           ")
    print("====================================================================*/")
    print(bieu_do_ngay_sinh)

    print("*=====================================================================")
    print("                            BIỂU ĐỒ HỌ TÊN                            ")
    print("====================================================================*/")
    print(bieu_do_ho_ten)

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(612, 900))

    # Chiều cao default text ban đầu
    highest = 817
    fullname_front = 'Vietnamese-coiny-Front'
    fullname_front1 = 'Vietnamese-coiny-Front1'
    pdfmetrics.registerFont(TTFont(fullname_front1, 'Faustina-BoldItalic.ttf'))
    pdfmetrics.registerFont(TTFont(fullname_front, 'Faustina-SemiBold.ttf'))

    # Drawing Name & Date
    can.setFont(fullname_front1, 18)
    can.setFillColor(reportlab.lib.colors.purple)

    can.drawString(139, highest, str(full_name).upper())

    can.drawString(465, highest, str(birthday.replace("-", "/")))


    can.setFont(fullname_front, 22)
    width1 = 96
    width2 = 185
    width3 = 265
    width4 = 350
    width5 = 430
    width6 = 515
    ## Xử lý ngoại lệ các trường hợp có nhiều ký tự
    width_solap = width3 - chi_so_lap.count(',') * 8
    width_baihocnghiep = width5 - chi_so_bai_hoc_nghiep.count(',') * 8
    width_nonghiep = width6 - chi_so_no_nghiep.count(',') * 8
    width_damme = width6 - chi_so_dam_me.count(',') * 8
    width_noi_tam = width_tuong_tac = width_ca_nhan = width1
    width_su_menh = width2
    width_duong_doi = width3
    width_ngay_sinh = width4
    width_truong_thanh = width5


    # Drawing the 1st line
    high = highest - 145
    can.setFillColor(reportlab.lib.colors.red)
    if len(chi_so_noi_tam) > 3:
        width_noi_tam = width1 - 10

    can.drawString(width_noi_tam, high, chi_so_noi_tam)
    can.setFillColorRGB(199 / 255, 12 / 255, 129 / 255)
    can.drawString(width2, high, str(chi_so_tiem_thuc))
    can.drawString(width3, high, chi_so_logic)
    width_cam_xuc = width4
    if len(chi_so_su_menh) > 3:
        width_cam_xuc = width4 - 10
    can.drawString(width_cam_xuc, high, chi_so_cam_xuc)
    can.drawString(width5, high, chi_so_truc_giac)
    can.drawString(width6, high, chi_so_trai_nghiem)

    # Drawing the 2rd line
    high = highest - 237
    can.setFillColor(reportlab.lib.colors.red)
    if len(chi_so_tuong_tac) > 3:
        width_tuong_tac = width1 - 10
    can.drawString(width_tuong_tac, high, chi_so_tuong_tac)
    can.setFillColorRGB(199 / 255, 12 / 255, 129 / 255)
    can.drawString(width2, high, chi_so_thai_do)
    can.drawString(width_solap, high, chi_so_lap)
    can.drawString(width4, high, chi_so_can_bang)
    can.drawString(width_baihocnghiep, high, chi_so_bai_hoc_nghiep)
    can.drawString(width_nonghiep, high, chi_so_no_nghiep)

    # Drawing the 3rd line
    high = highest - 337
    can.setFillColor(reportlab.lib.colors.red)
    if len(nam_ca_nhan) > 3:
        width_ca_nhan = width1 - 10
    can.drawString(width_ca_nhan, high, nam_ca_nhan)
    if len(chi_so_su_menh) > 3:
        width_su_menh = width2 - 10
    can.drawString(width_su_menh, high, chi_so_su_menh)
    if len(chi_so_duong_doi) > 3:
        width_duong_doi = width3 - 10
    can.drawString(width_duong_doi, high, chi_so_duong_doi)
    if len(chi_so_ngay_sinh) > 3:
        width_ngay_sinh = width4 - 10
    can.drawString(width_ngay_sinh, high, chi_so_ngay_sinh)
    if len(chi_so_truong_thanh) > 3:
        width_truong_thanh = width5 - 10
    can.drawString(width_truong_thanh, high, chi_so_truong_thanh)
    if len(chi_so_dam_me) > 7:
        can.setFont(fullname_front, 18)
        width_damme = width_damme + 5
    can.drawString(width_damme, high, chi_so_dam_me)
    # Drawing biểu đồ đường đời

    width_dinh4 = 198
    width_dinh3 = 198
    width_dinh2 = 243
    width_dinh1 = 149
    width_dinh0_1 = 91
    width_dinh0_2 = 296
    width_dinh0_3 = 198
    if (len(bieu_do_duong_doi[6]) > 3):
        width_dinh4 = 190
    if (len(bieu_do_duong_doi[5]) > 3):
        width_dinh3 = 190
    if (len(bieu_do_duong_doi[4]) > 3):
        width_dinh2 = 237
    if (len(bieu_do_duong_doi[3]) > 3):
        width_dinh1 = 141

    if (len(bieu_do_duong_doi[1]) > 3):
        width_dinh0_1 = 83
    if (len(bieu_do_duong_doi[2]) > 3):
        width_dinh0_2 = 288
    if (len(chi_so_ngay_sinh) > 3):
        width_dinh0_3 = 190


    can.setFont(fullname_front, 11)

    can.drawString(width_dinh4, 415, bieu_do_duong_doi[6])
    can.drawString(width_dinh3, 348, bieu_do_duong_doi[5])
    can.drawString(width_dinh2, 297, bieu_do_duong_doi[4])
    can.drawString(width_dinh1, 297, bieu_do_duong_doi[3])
    can.drawString(width_dinh0_1, 240, bieu_do_duong_doi[1])
    can.drawString(width_dinh0_2, 240, bieu_do_duong_doi[2])
    # can.drawString(195, 240, bieu_do_duong_doi[0]) Ngoại lệ lấy chỉ số đường đời
    can.drawString(width_dinh0_3, 240, chi_so_ngay_sinh)

    # can.drawString(width_dinh4, 415, '12/4')
    # can.drawString(width_dinh3, 348, '12/4')
    # can.drawString(width_dinh2, 297, '12/4')
    # can.drawString(width_dinh1, 297, '12/4')
    # can.drawString(width_dinh0_1, 240, '1')
    # can.drawString(width_dinh0_2, 240, '1')
    # # can.drawString(195, 240, bieu_do_duong_doi[0]) Ngoại lệ lấy chỉ số đường đời
    # can.drawString(width_dinh0_3, 240, '1')

    # Drawing more infomation
    can.setFillColorRGB(199 / 255, 12 / 255, 129 / 255)
    can.drawString(130, 260, f"0 - {age_range}")
    can.drawString(225, 260, f"{age_range + 1} - {age_range + 9}")
    can.drawString(180, 315, f"{age_range + 10} - {age_range + 18}")
    can.drawString(180, 375, f"{age_range + 19} - {age_range + 27}")

    # Drawing Nội tâm và tương tác , sứ mệnh và dường đời
    can.setFont(fullname_front, 22)
    can.setFillColorRGB(199 / 255, 12 / 255, 129 / 255)
    can.drawString(110, 100, chi_so_noi_tam_va_tuong_tac)
    can.drawString(190, 100, chi_so_su_menh_va_duong_doi)

    # Drawing bieu do ikigai (3 vòng tròn)
    can.setFont(fullname_front, 16)
    can.setFillColor(reportlab.lib.colors.red)
    if dam_me:
        dam_me = ",".join(map(str, dam_me))
    else:
        dam_me = ""
    if chuyen_mon:
        chuyen_mon = ",".join(map(str, chuyen_mon))
    else:
        chuyen_mon = ""
    if su_nghiep:
        su_nghiep = ",".join(map(str, su_nghiep))
    else:
        su_nghiep = ""
    width_dam_me = 395 - dam_me.count(',') * 5
    can.drawString(width_dam_me, 350, str(dam_me))
    can.drawString(468, 350, chi_so_su_menh.split("/")[1] if "/" in chi_so_su_menh else chi_so_su_menh)

    width_chuyen_mon = 395 - chuyen_mon.count(',') * 5
    width_su_nghiep = 470 - su_nghiep.count(',') * 5
    can.drawString(width_chuyen_mon, 270, str(chuyen_mon))
    can.drawString(width_su_nghiep, 270, str(su_nghiep))

    # Drawing 2 bảng sau cùng
    can.setFont(fullname_front, 11)
    can.setFillColor(reportlab.lib.colors.red)

    number_1 = bieu_do_ngay_sinh.get(1)
    number_2 = bieu_do_ngay_sinh.get(2)
    number_3 = bieu_do_ngay_sinh.get(3)
    number_4 = bieu_do_ngay_sinh.get(4)
    number_5 = bieu_do_ngay_sinh.get(5)
    number_6 = bieu_do_ngay_sinh.get(6)
    number_7 = bieu_do_ngay_sinh.get(7)
    number_8 = bieu_do_ngay_sinh.get(8)
    number_9 = bieu_do_ngay_sinh.get(9)

    high_line1 = 80
    high_line2 = 120
    high_line3 = 160
    if number_1:
        x = 266 - number_1 * 2.5
        for _ in range(0, number_1):
            can.drawString(x, high_line1, "1")
            x += 7
    if number_2:
        x = 266 - number_2 * 2.5
        for _ in range(0, number_2):
            can.drawString(x, high_line2, "2")
            x += 7
    if number_3:
        x = 266 - number_3 * 2.5
        for _ in range(0, number_3):
            can.drawString(x, high_line3, "3")
            x += 7
    if number_4:
        x = 310 - number_4 * 2.5
        for _ in range(0, number_4):
            can.drawString(x, high_line1, "4")
            x += 7
    if number_5:
        x = 310 - number_5 * 2.5
        for _ in range(0, number_5):
            can.drawString(x, high_line2, "5")
            x += 7
    if number_6:
        x = 310 - number_6 * 2.5
        for _ in range(0, number_6):
            can.drawString(x, high_line3, "6")
            x += 7
    if number_7:
        x = 355 - number_7 * 2.5
        for _ in range(0, number_7):
            can.drawString(x, high_line1, "7")
            x += 7
    if number_8:
        x = 355 - number_8 * 2.5
        for _ in range(0, number_8):
            can.drawString(x, high_line2, "8")
            x += 7
    if number_9:
        x = 355 - number_9 * 2.5
        for _ in range(0, number_9):
            can.drawString(x, high_line3, "9")
            x += 7

    name_1 = bieu_do_ho_ten.get(1)
    name_2 = bieu_do_ho_ten.get(2)
    name_3 = bieu_do_ho_ten.get(3)
    name_4 = bieu_do_ho_ten.get(4)
    name_5 = bieu_do_ho_ten.get(5)
    name_6 = bieu_do_ho_ten.get(6)
    name_7 = bieu_do_ho_ten.get(7)
    name_8 = bieu_do_ho_ten.get(8)
    name_9 = bieu_do_ho_ten.get(9)

    if name_1:
        x = 440 - name_1 * 2.5
        for _ in range(0, name_1):
            can.drawString(x, high_line1, "1")
            x += 7
    if name_2:
        x = 440 - name_2 * 2.5
        for _ in range(0, name_2):
            can.drawString(x, high_line2, "2")
            x += 7
    if name_3:
        x = 440 - name_3 * 2.5
        for _ in range(0, name_3):
            can.drawString(x, high_line3, "3")
            x += 7
    if name_4:
        x = 485 - name_4 * 2.5
        for _ in range(0, name_4):
            can.drawString(x, high_line1, "4")
            x += 7
    if name_5:
        x = 485 - name_5 * 2.5
        for _ in range(0, name_5):
            can.drawString(x, high_line2, "5")
            x += 7
    if name_6:
        x = 485 - name_6 * 2.5
        for _ in range(0, name_6):
            can.drawString(x, high_line3, "6")
            x += 7
    if name_7:
        x = 530 - name_7 * 2.5
        for _ in range(0, name_7):
            can.drawString(x, high_line1, "7")
            x += 7
    if name_8:
        x = 530 - name_8 * 2.5
        for _ in range(0, name_8):
            can.drawString(x, high_line2, "8")
            x += 7
    if name_9:
        x = 530 - name_9 * 2.5
        for _ in range(0, name_9):
            can.drawString(x, high_line3, "9")
            x += 7
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("result.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file

    outputStream = open("output.pdf", "wb")
    output.write(outputStream)
    outputStream.close()




def merge_pdfs(_pdfs):
    mergeFile = PyPDF2.PdfFileMerger()
    for _pdf in _pdfs:
        mergeFile.append(PyPDF2.PdfFileReader(_pdf, 'rb'))
    mergeFile.write("output1.pdf")
    mergeFile.close()



if __name__ == '__main__':
    main()

