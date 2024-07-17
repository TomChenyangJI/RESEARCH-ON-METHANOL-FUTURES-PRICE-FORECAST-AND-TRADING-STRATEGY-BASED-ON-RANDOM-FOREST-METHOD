import xlrd
from xlrd.xldate import xldate_as_datetime
import xlwt
import time
import datetime
from 获取指定日期的星期数 import get_yesterday
from 匹配两个Excel中的数据对 import makeDir



# book = xlrd.open_workbook(future_path)
# sheet = book.sheets()[0]
# print(sheet.nrows)

# 获取一个Excel文件中的数据
def get_data(excel_path, *args):
    """
    这个函数是用来获取excel_path中的数据的
    :param excel_path: Excel文件所在的路径，可以是绝对路径，也可以是当前文件夹的相对路径
    :param args: 要获取的Excel文件中的哪些列的数据
    :return: 返回的值是一个字典数据类型，其key是日期，值是数组
    """
    # args 是用来放列的数字的,格式是tuple
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    data_dict = {}
    print(excel_path)
    print(rows)
    # 提取数据
    for row in range(1, rows):
        temp_list = []
        for i in args:
            # i代表的是列数
            i_val = sheet.cell_value(row, i) # 数据
            temp_list.append(i_val)
        i_key = sheet.cell_value(row, 0) # date
        if '-' in i_key:
            data_dict[i_key.replace('-', '')] = temp_list
            pass
        else:
            data_dict[str(int(i_key))] = temp_list

    return data_dict

def get_future_data(future_path, *args):
    """
        这个函数是用来获取future_path中的数据的，仅限于用来获取大智慧客户端保存下来的Excel文件，它
        的特别之处在于它的日期格式在Excel中是datetime格式的
        :param excel_path: Excel文件所在的路径，可以是绝对路径，也可以是当前文件夹的相对路径
        :param args: 要获取的Excel文件中的哪些列的数据
        :return: 返回的值是一个字典数据类型，其key是日期，值是数组
        """
    # args 是用来放列的数字的,格式是tuple
    book = xlrd.open_workbook(future_path)
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    data_dict = {}

    # 提取数据
    for row in range(1, rows):
        temp_list = []
        for i in args:
            # i代表的是列数
            i_val = sheet.cell_value(row, i)  # 数据
            temp_list.append(i_val)
        i_key = sheet.cell_value(row, 0)  # date
        i_key = xldate_as_datetime(i_key, '').strftime('%Y%m%d')
        data_dict[i_key] = temp_list

    return data_dict


# 将两个数据进行错开匹配
def move_match(future_path, other_path, f_col, o_col):
    """
    将两个Excel文件中的数据进行匹配，主要是将第一个Excel文件的日期（比如说"20200102"）与第二个文件中的
    前一天的日期进行（比如说"20200101"）错开匹配
    :param future_path: 第一个Excel文件的地址
    :param other_path: 第二个Excel文件的地址
    :return: 返回一个字典，其key为日期，格式为"2020-01-01"，值为数组，数组的第一个元素为第一个Excel文件中的数据（如：期货数据），
    第二个元素为第二个Excel文件中的数据（如：现货的数据）
    """
    match_dict = {}
    future_data = get_future_data(future_path, f_col) # 第一个文件（期货）的数据
    other_data = get_data(other_path, o_col) # 第二个文件（比如说"现货"）的数据
    # other_data = get_future_data(other_path, o_col) # 第二个文件（比如说"现货"）的数据
    # 以期货数据为主
    other_all_dates = list(other_data.keys())
    for date in list(future_data.keys()):
        match_date = get_yesterday(date)
        if match_date in other_all_dates:
            # 说明匹配到了
            match_dict[date] = [future_data[date], other_data[match_date]]

    return match_dict


#
# result = get_future_data(future_path, 4)
# print(result)

# result = move_match(future_path, other_path, 4, 1) # 为两个Excel中错开匹配的数据，但是是升序的
# # 获取到错开匹配的数据之后就要进行数据的写入了
# # 要保存的文件的路径的base_path
# base_path = '~/Desktop/ 小论文/数据/将数据错开后进行匹配'
# save_path = base_path + '/' + other_path.split('/')[-2]

# makeDir(save_path)
# for key in list(result.keys()):
#
#     pass

def save_data(future_path, other_path, f_col, o_col):
    result = move_match(future_path, other_path, f_col, o_col)
    base_path = '~/Desktop/ 小论文/数据/将数据错开后进行匹配'
    save_path = base_path + '/' + other_path.split('/')[-2]
    makeDir(save_path)
    book = xlwt.Workbook(other_path.split('/')[-1])
    sheet = book.add_sheet('sheet1')
    # 进行数据的写入操作
    sheet.write(0, 0, '日期')
    sheet.write(0, 1, '期货价格')
    sheet.write(0, 2, "其他数据")
    i = 0
    for key in list(result.keys()):
        i += 1
        sheet.write(i, 0, key)
        sheet.write(i, 1, result[key][0][0])
        sheet.write(i, 2, result[key][1][0])

    book.save(save_path + '/期货价格_' + other_path.split('/')[-1].split('.')[0] + '.xls')

#
future_path = '~/Desktop/ 小论文/数据/期货数据/螺纹钢期货-大智慧.xlsx'
other_path = '~/Desktop/ 小论文/数据/期货数据/焦炭期货-大智慧.xlsx'

save_data(future_path, other_path, 4, 1)

# 其他期货数据从大智慧进行下载