import xlrd
import math
import os


def get_data(excel_path):
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    data = []
    for row in range(1, rows):
        tmp = []
        for col in range(cols):
            val = sheet.cell_value(row, col)
            tmp.append(val)
        data.append(tmp)
    return data

def get_income(excel_path, txt_file='~/Desktop/论文研究/甲醇/交易策略数据/策略实验结果/最终选定的策略/策略收益.txt'):
    para = excel_path.split('/')[-1][:-4].strip()
    file_obj = open(txt_file, 'r')
    lines = file_obj.readlines()
    file_obj.close()
    income = 0
    for line in lines:
        para_ = line.split(' ')[0]
        if para == para_:
            income = float(line.split(' ')[-1])
            break
    first_three_parameter = para
    return first_three_parameter, income


def get_std(excel_path):
    data = get_data(excel_path)
    price = [i[1] for i in data]
    collection_rate = []
    for i in range(1, len(price)):
        pres_record = price[i]
        prev_record = price[i - 1]
        rate = (pres_record - prev_record) / prev_record
        collection_rate.append(rate)
    ave = sum(collection_rate) / len(collection_rate)
    std = math.sqrt(sum([(i - ave)*(i - ave) for i in collection_rate]) / (len(collection_rate)-1))
    return std  # 日收益率的标准差


def sharpRate(excel_path, txt_file='~/Desktop/论文研究/甲醇/交易策略数据/策略实验结果/最终选定的策略/策略收益.txt'):
    rate = 0.031
    data = get_data(excel_path)
    dest = [(i[1] if (i[-1] == 1 or i[-1] == -1) else 0) for i in data]
    input = max(dest)
    first_three_parameter, income = get_income(excel_path, txt_file)
    Erp = income / input / 5
    qp = get_std(excel_path)
    sharp = (Erp - rate) / qp

    return first_three_parameter, income, sharp  # 返回的值就是 夏普比率



# sharpRate('~/Desktop/论文研究/甲醇/交易策略数据/策略实验结果/最终选定的策略/47_0.9_0.6.xls')

dir_path = '~/Desktop/论文研究/甲醇/交易策略数据/策略实验结果/最终选定的交易策略2'
excel_list = []
for i in os.listdir(dir_path):
    if i.split('.')[-1] == 'xls':
        excel_list.append(os.path.join(dir_path, i))

file_obj = open('~/Desktop/论文研究/甲醇/交易策略数据/策略实验结果/最终选定的交易策略2/策略夏普率.txt', 'a+')
for excel_path in excel_list:
    first_three_parameter, income, sharp = sharpRate(excel_path)
    file_obj.write(f'{first_three_parameter}\t{income}\t夏普比率{sharp}\n')

    # print(first_three_parameter, income, sharp)
file_obj.close()