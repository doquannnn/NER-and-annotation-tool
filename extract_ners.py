import re
NERS  = ["PERSON", "LOCATION", "ORGANIZATION", "MISCELLANEOUS"]


def case1(s):
    text_inside = re.findall("<ENAMEX.+?>(.+?)<\.?/ENAMEX.?>", s)[0]
    label = re.findall('<ENAMEX.?TYPE="?(.+)?">', s)[0]

    return [(text_inside, label)]


def case2(s):
    temp = re.findall("<ENAMEX.+?>(.+?)<\.?/ENAMEX.?>", s)[0]
    text_insides = list(map(lambda s: s.strip(), re.split("<.+?>", temp)))

    labels, check_first = [], []
    for NER in NERS:
        idxs = [_.start() for _ in re.finditer(NER, s)]
        if len(idxs) != 0:
            for idx in idxs:
                labels.append(NER)
                check_first.append(idx)

    if check_first[0] < check_first[1]:

        return list(zip(text_insides, labels))

    return list(zip(text_insides, labels[::-1]))



# corner case example:
cc1 = 'Cũng theo nhận định từ <ENAMEX TYPE="ORGANIZATION">Công ty Cổ phần Cao su \
    <ENAMEX TYPE="LOCATION">Bình Dương</ENAMEX></ENAMEX>, giá cao su tăng mạnh \
    vào cuối năm 2016 phần lớn là do thị trường <ENAMEX TYPE="LOCATION">Trung Quốc</ENAMEX>\
     mở cửa. Cụ thể giá cao su tăng mạnh vào đầu năm 2017 là do nhu cầu sản xuất lốp xe tại \
    <ENAMEX TYPE="LOCATION">Trung Quốc</ENAMEX> đang có xu hướng phục hồi. Trước đó, ông \
    <ENAMEX TYPE="PERSON">Shinichi Kato</ENAMEX>, Chủ tịch bộ phận Giao dịch cao su nguyên liệu \
    tại <ENAMEX TYPE="ORGANIZATION"><ENAMEX TYPE="PERSON">Shinichi Kato</ENAMEX> Office</ENAMEX>\
 (<ENAMEX TYPE="LOCATION">Nhật Bản</ENAMEX>) cũng dự đoán nhu cầu sản xuất lốp xe tại\
<ENAMEX TYPE="LOCATION">Trung Quốc</ENAMEX> đang tăng và giá cao su sẽ còn ở mức cao cho \
    đến tháng 4/2017.'

cc2 = '<ENAMEX TYPE="ORGANIZATION">ban dân vận <ENAMEX TYPE="ORGANIZATION">huyện ủy \
    <ENAMEX TYPE="LOCATION">Đắk G’long</ENAMEX></ENAMEX></ENAMEX> \
        (<ENAMEX TYPE="LOCATION">Đắk Nông</ENAMEX>)'

