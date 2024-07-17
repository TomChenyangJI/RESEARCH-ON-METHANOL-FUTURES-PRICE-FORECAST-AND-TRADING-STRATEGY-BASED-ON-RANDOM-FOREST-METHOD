import os
import xlrd




def read_excel(path):
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    data = []
    for row in range(1, rows):
        record = []
        for col in range(cols):
            val = sheet.cell_value(row, col)
            record.append(val)
        data.append(record)
    return data


# 对数据进行处理
def dispose_data(data):
    one_tag = 0
    minus_tag = 0
    zero_tag = 0
    length = len(data)
    index = 0
    long_start = 0
    short_start = 0
    income = 0
    while index < length:
        record = data[index]
        tag = record[-1]
        if tag == 2:
            index += 1
        else:
            index += 1
            if zero_tag == 0:
                if tag == 1:
                    zero_tag = 1
                    long_start = record[1]
                    one_tag = 1
                elif tag == -1:
                    zero_tag = 1
                    short_start = record[1]
                    minus_tag = 1
            else:
                # 这个时候说明tag的值是0
                if tag == 0:
                    # print(f'判断是正确的{zero_tag}')
                    zero_tag = 0
                    if one_tag == 1:
                        price = record[1]
                        income += (price - long_start)
                        one_tag = 0
                    if minus_tag == 1:
                        price = record[1]
                        income += (short_start - price)
                        minus_tag = 0
    return income


dir_path = '~/Desktop/论文研究/甲醇/交易策略数据/策略实验结果'
file_obj = open(dir_path + '/策略收益.txt', 'a+')
t = os.listdir(dir_path)
for ele in t:
    if ele.split('.')[-1] == 'xls':
        data = read_excel(os.path.join(dir_path, ele))
        income = dispose_data(data)
        string = ele[:10] + '  ' + str(income) + '\n'
        file_obj.write(string)

file_obj.close()