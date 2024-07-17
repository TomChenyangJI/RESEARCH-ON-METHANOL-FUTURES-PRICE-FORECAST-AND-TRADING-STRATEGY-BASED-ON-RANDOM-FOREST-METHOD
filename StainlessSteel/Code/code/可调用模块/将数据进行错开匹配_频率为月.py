import time
import xlwt

from 获取指定日期的星期数 import getSpecificDay, get_next_day
from 将数据进行错开匹配_频率为日 import get_data, get_future_data
from 匹配两个Excel中的数据对 import makeDir


def abbr_to_full(date):
    """

    :param date: 格式为"20200101"
    :return: 格式为"2020-01-01"
    """
    return date[0:4] + '-' + date[4:6] + '-' + date[6:]


def next_day_match(future_excel, other_excel, f_col, o_col):
    """
    将所要匹配数据的后一天数据与这个数据进行匹配，比如周数据为2021-05-21这一天的数据，与日数据的2021-05-24这一天的数据进行匹配
    这个逻辑似乎更有说服力
    :param future_excel: 期货数据Excel文件的所在路径
    :param other_excel: 其他数据（例如：现货）Excel文件所在的路径
    :param f_col: 要获取的期货数据Excel文件中的第几列数据
    :param o_col: 要获取的其他数据（例如：现货）Excel文件中的第几列数据
    :return: 返回值为一个字典，字典的key为日期，格式为"20200101"，键为列表，列表的第一个元素是期货的数据，第二个元素是其他
    Excel文件中的数据
    """
    other_data = get_data(other_excel, o_col)
    future_data = get_future_data(future_excel, f_col)

    future_dday = list(future_data.keys())
    return_dict = {}
    for dday in list(other_data.keys()):
        result = get_next_day(abbr_to_full(dday))
        temp = dday
        while True:
            if temp in future_dday:
                # 说明找到下一天的数据，及时停止
                # temp 是期货的日期
                # print(future_data[temp])
                # print(float(other_data[dday][0].strip()))
                # print(future_data)
                try:
                    return_dict[temp] = [future_data[temp][0],float(other_data[dday][0].strip())]
                except AttributeError:
                    return_dict[temp] = [future_data[temp][0],other_data[dday][0]]
                break
            else:
                temp = get_next_day(abbr_to_full(temp)).replace('-', '')

    return return_dict

def save_data(future_excel, other_excel, f_col, o_col, save_base_path):
    makeDir(save_base_path)
    future_filename = future_excel.split('/')[-1].split('.')[0]
    other_filename = other_excel.split('/')[-1].split('.')[0]
    result_dict = next_day_match(future_excel, other_excel, f_col, o_col)
    # print(result_dict)
    # 将数据写入到Excel文件中
    book = xlwt.Workbook(f'{other_filename}.xls')
    sheet = book.add_sheet('sheet1')
    sheet.write(0, 0, '日期')
    sheet.write(0, 1, '期货价格')
    sheet.write(0, 2, '其他数据')

    i = 0
    for key in list(result_dict.keys()):
        i += 1
        sheet.write(i, 0, key)
        sheet.write(i, 1, result_dict[key][0])
        sheet.write(i, 2, result_dict[key][1])

    book.save(save_base_path + f'/^{future_filename}_{other_filename}.xls')

future_path = '~/Desktop/ 小论文/数据/螺纹钢期货-大智慧.xlsx'
other_path = '~/Desktop/ 小论文/数据/进出口/红期-焦炭进口金额.xlsx'

base_path = '~/Desktop/ 小论文/数据/将数据错开后进行匹配/进出口/使用转换月数据的程序处理的结果'

save_data(future_path, other_path, 4, 1, base_path)
