import xlwt
import xlrd
from xlrd import xldate_as_datetime
import datetime
import time
import os


def getData(excel_path, col):
    """
    用来获取指定Excel文件中指定列的数据，以字典的格式返回
    :param excel_path: Excel文件绝对路径
    :param col: 指定列
    :return: 返回值是字典，key为日期，val为对应的col列的数据
    """
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    data = {}
    for i in range(1, rows):
        key = str(int(sheet.cell_value(i, 0)))
        val = sheet.cell_value(i, col)
        data[key] = val
    return data


def getFutureData(future_path, col):
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
        # i代表的是列数
        temp_list = sheet.cell_value(row, col)  # 数据
        i_key = sheet.cell_value(row, 0)  # date
        i_key = xldate_as_datetime(i_key, '').strftime('%Y%m%d')
        data_dict[i_key] = temp_list
    return data_dict


def get_prev_weekdays(ddate):
    """
    用来获取这个日期以前的周的工作日期
    :param ddate: 输入的指定日期 格式为"20210524"
    :return: 返回一个列表，为本周此日期（ddate）以前的工作日
    """
    result = []
    today = ddate
    today = str(int(today))
    nth_week = datetime.datetime(int(today[0:4]), int(today[4: 6]), int(today[6:])).strftime('%W')
    delta = datetime.timedelta(-1)
    while True:
        datetime_obj = datetime.datetime(int(today[0:4]), int(today[4: 6]), int(today[6:]))
        in_nth_week = datetime_obj.strftime('%W')
        if in_nth_week == nth_week:
            result.append(datetime_obj.strftime('%Y%m%d'))
            datetime_obj += delta
            today = datetime_obj.strftime('%Y%m%d')
        else:
            break
    return result


def get_prev_monthdays(ddate, amount):
    """
    用来获取这个日期前一个月的工作日期
    :param ddate: 输入的指定日期 格式为"20210524"
    :return: 返回一个列表，为本周此日期（ddate）以前的工作日
    """
    result = []
    today = ddate
    nth_month = datetime.datetime(int(today[0:4]), int(today[4: 6]), int(today[6:])).strftime('%m')
    delta = datetime.timedelta(days=-1)
    count = 0
    while True:
        now_nth_month = datetime.datetime(int(today[0:4]), int(today[4: 6]), int(today[6:])).strftime('%m')
        datetime_obj = datetime.datetime(int(today[0:4]), int(today[4: 6]), int(today[6:]))
        # if now_nth_month == nth_month:
        #     result.append(datetime_obj.strftime('%Y%m%d'))
        #     datetime_obj += delta
        #     today = datetime_obj.strftime('%Y%m%d')
        # else:
        #     break
        if count <= amount:
            result.append(datetime_obj.strftime('%Y%m%d'))
            datetime_obj += delta
            today = datetime_obj.strftime('%Y%m%d')
            count += 1
        else:
            break
    return result


# 进行不同频率的数据的匹配分析
def week_generation(data):
    """
    此函数是将以周为频率的数据转换为以日为频率的数据，以周数据填充以前的数据
    :param data: 是字典数据类型，key是日期，val是值
    :return: 依旧是字典格式，key是日期，val经过处理之后的数据
    """
    result = {}
    date_li = list(data.keys())
    for key in date_li:
        val = data[key]
        result[key] = val
        weekdays = get_prev_weekdays(key)
        for weekday in weekdays:
            if weekday in date_li:
                continue
            else:
                result[weekday] = val
    return result


# 进行不同频率的数据的匹配分析--月
def month_generation(data, amount):
    """
    此函数是将以月为频率的数据转换为以日为频率的数据，以月数据填充以前的数据
    :param data: 是字典数据类型，key是日期，val是值
    :return: 依旧是字典格式，key是日期，val经过处理之后的数据
    """
    result = {}
    date_li = list(data.keys())
    date_li.sort(reverse=1)
    for key in date_li:
        val = data[key]
        result[key] = val
        monthdays = get_prev_monthdays(key, amount)
        for monthday in monthdays:
            if monthday in date_li:
                continue
            else:
                result[monthday] = val
    return result


def match_data(data1, data2): # 这个函数写的不好，要重新写一下
    """
    将两个字典类型的数据进行匹配，以第一个字典中的数据为基准进行比较
    :param data1: 第一个字典 为期货价格数据
    :param data2: 第二个字典 为其他数据
    :return: 返回匹配过后的两个字典
    """
    result = {}
    key_li1 = data1.keys()
    key_li2 = data2.keys()
    for key in key_li1:
        if key in key_li2:
            result[key] = [data1[key], data2[key]]
    return result

def makeDir(path):
    """

    :param path: 创建文件夹路径
    :return: None
    """
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
