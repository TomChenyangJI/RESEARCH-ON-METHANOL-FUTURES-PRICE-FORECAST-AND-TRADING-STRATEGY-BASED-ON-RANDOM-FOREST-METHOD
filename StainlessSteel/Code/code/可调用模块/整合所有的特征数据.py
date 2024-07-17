"""
            螺纹钢                    焦炭                       焦煤                          铁矿石
期货价格     现货价格                   现货价格                     现货价格                    现货价格
            期货价格                   期货价格                     期货价格                    期货价格
            开工率                     开工率                       开工率                     开工率
            毛利                      毛利                          毛利                      毛利
            进出口                    进出口                                                进出口
                                     库存                          库存                      库存
"""

import xlwt
import xlrd
from xlrd import xldate_as_datetime
import datetime
import time


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
        key = sheet.cell_value(i, 0)
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


def get_prev_monthdays(ddate):
    """
    用来获取这个日期前一个月的工作日期
    :param ddate: 输入的指定日期 格式为"20210524"
    :return: 返回一个列表，为本周此日期（ddate）以前的工作日
    """
    result = []
    today = ddate
    nth_month = datetime.datetime(int(today[0:4]), int(today[4: 6]), int(today[6:])).strftime('%m')
    delta = datetime.timedelta(days=-1)
    while True:
        now_nth_month = datetime.datetime(int(today[0:4]), int(today[4: 6]), int(today[6:])).strftime('%m')
        datetime_obj = datetime.datetime(int(today[0:4]), int(today[4: 6]), int(today[6:]))
        if now_nth_month == nth_month:
            result.append(datetime_obj.strftime('%Y%m%d'))
            datetime_obj += delta
            today = datetime_obj.strftime('%Y%m%d')
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
def month_generation(data):
    """
    此函数是将以月为频率的数据转换为以日为频率的数据，以月数据填充以前的数据
    :param data: 是字典数据类型，key是日期，val是值
    :return: 依旧是字典格式，key是日期，val经过处理之后的数据
    """
    result = {}
    date_li = list(data.keys())
    for key in date_li:
        val = data[key]
        result[key] = val
        monthdays = get_prev_monthdays(key)
        for monthday in monthdays:
            if monthday in date_li:
                continue
            else:
                result[monthday] = val
    return result


def match_data(data1, data2):
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


def integral_week(future_path, col1, other_path, col2):
    future_data = getData(future_path, col1)
    other_data = getData(other_path, col2)
    other_data = week_generation(other_data)
    match_result = match_data(future_data, other_data)
    return match_result


# 命名的规范
# 现货 spot
# 库存 inventory
# 进出口 im_ex
# 开工率 op_rate
# 毛利profit
# 期货价格 future_price
# 品种名 steel螺纹钢 coal焦炭 ore铁矿石 coking焦煤

# 获取 期货价格 日数据
future_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/期货数据/铁矿石期货-大智慧.xlsx', 4],
    '焦煤': ['~/Desktop/ 小论文/数据/期货数据/焦煤期货-大智慧.xlsx', 4],
    '焦炭': ['~/Desktop/ 小论文/数据/期货数据/焦炭期货-大智慧.xlsx', 4],
    '螺纹钢': ['~/Desktop/ 小论文/数据/期货数据/螺纹钢期货-大智慧.xlsx', 4]
}

# 技术指标 日数据

# 获取 现货价格 日数据
spot_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/现货数据/期货价格_铁矿石_澳.xls', 2],
    '焦煤': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/现货数据/期货价格_炼焦煤.xls', 2],
    '焦炭': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/现货数据/期货价格_焦炭.xls', 2],
    '螺纹钢': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/现货数据/期货价格_螺纹钢.xls', 2]
}

# 获取 开工率 月数据好像 周 半月数据
rate_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/开工率/以周（半月）数据为基准/^螺纹钢期货-大智慧_铁矿石_国产矿山开工率.xls', 2],
    '焦煤': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/开工率/以周（半月）数据为基准/^螺纹钢期货-大智慧_焦煤_山西大同煤矿开工率.xls', 2],
    '焦炭': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/开工率/以周（半月）数据为基准/^螺纹钢期货-大智慧_焦炭_焦炭中国周度开工率.xls', 2],
    '螺纹钢': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/开工率/以周（半月）数据为基准/^螺纹钢期货-大智慧_螺纹钢_建筑钢材产线开工率.xls', 2]
}

# 获取 毛利 日数据
profit_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/毛利/期货价格_铁矿石_唐山地区钢坯利润.xls', 2],
    '焦煤': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/毛利/期货价格_焦煤_炼焦煤毛利.xls', 2],
    '焦炭': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/毛利/期货价格_焦炭_山西焦炭毛利.xls', 2],
    '螺纹钢': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/毛利/期货价格_螺纹钢_螺纹钢毛利.xls', 2]
}

# 获取 进出口 月数据
im_ex_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/进出口/以月数据为基准/^螺纹钢期货-大智慧_铁矿石_铁矿：进口数量合计：全球—中国（月）.xls', 2],
    '焦煤': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/进出口/以月数据为基准/^螺纹钢期货-大智慧_焦煤_进口炼焦煤：港口库存合计（周）.xls', 2],
    '焦炭': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/进出口/以月数据为基准/^螺纹钢期货-大智慧_焦炭_焦炭：进口数量合计：省市：中国（月）.xls', 2],
# 这个数据是直接不要了的我记得
    '螺纹钢': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/进出口/以月数据为基准/^螺纹钢期货-大智慧_螺纹钢_螺纹钢：出口数量：中国（月）.xls', 2]
}

# 获取 库存 周
inventory_path = {
    '铁矿石': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/库存/以周数据为基准/^螺纹钢期货-大智慧_卓_铁矿石_澳矿库存情况.xls', 2],
    '焦煤': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/库存/以周数据为基准/^螺纹钢期货-大智慧_焦煤_炼焦煤：110家钢铁企业：库存：中国（周）.xls', 2],
    '焦炭': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/库存/以周数据为基准/^螺纹钢期货-大智慧_焦炭_焦炭：110家钢铁企业：库存（周）.xls', 2],
    '螺纹钢': ['~/Desktop/ 小论文/数据/将数据错开后进行匹配/库存/以周数据为基准/^螺纹钢期货-大智慧_螺纹钢_螺纹钢：建筑钢材钢铁企业：库存：中国（周）.xls', 2]
}

# 字典中品种的顺序是：铁矿石 焦煤 焦炭 螺纹钢


# 是否需要将期货数据的日期格式修改为'20210524'

# 来想一下接下来的一步工作是什么
# 提取错开的月数据或者是周数据，然后将它们补充为日数据，然后进行所有数据的匹配
#
# 看一下哪些数据是不要的
# 焦炭的进出口 螺纹钢的库存不要

# 周数据 和 月数据

# 库存 --------------------------------------------------------
# 1.周数据
#焦炭
inve_coal = week_generation(getData(inventory_path['焦炭'][0], inventory_path['焦炭'][1]))
#铁矿石
inve_ore = week_generation(getData(inventory_path['铁矿石'][0], inventory_path['铁矿石'][1]))
#焦煤
inve_coking = week_generation(getData(inventory_path['焦煤'][0], inventory_path['焦煤'][1]))

# 开工率 --------------------------------------------------------
# 2.月数据
# 开工率
# 铁矿石
rate_ore = month_generation(getData(rate_path['铁矿石'][0], rate_path['铁矿石'][1]))
# 焦煤
rate_coking = month_generation(getData(rate_path['焦煤'][0], rate_path['焦煤'][1]))
# 焦炭
rate_coal = month_generation(getData(rate_path['焦炭'][0], rate_path['焦炭'][1]))
# 螺纹钢
rate_steel = month_generation(getData(rate_path['螺纹钢'][0], rate_path['螺纹钢'][1]))

# 进出口 --------------------------------------------------------
# 月数据
# 铁矿石
im_ex_ore = month_generation(getData(im_ex_path['铁矿石'][0], im_ex_path['铁矿石'][1]))
# 焦煤
im_ex_coking = month_generation(getData(im_ex_path['焦煤'][0], im_ex_path['焦煤'][1]))
# 焦炭
im_ex_coal = month_generation(getData(im_ex_path['焦炭'][0], im_ex_path['焦炭'][1]))
# 螺纹钢
im_ex_steel = month_generation(getData(im_ex_path['螺纹钢'][0], im_ex_path['螺纹钢'][1]))

# 毛利 --------------------------------------------------------
# 铁矿石
profit_ore = getData(profit_path['铁矿石'][0], profit_path['铁矿石'][1])
# 焦煤
profit_coking = getData(profit_path['焦煤'][0], profit_path['焦煤'][1])
# 焦炭
profit_coal = getData(profit_path['焦炭'][0], profit_path['焦炭'][1])
# 螺纹钢
profit_steel = getData(profit_path['螺纹钢'][0], profit_path['螺纹钢'][1])

# 期货 --------------------------------------------------------
# 铁矿石
future_ore = getFutureData(future_path['铁矿石'][0], future_path['铁矿石'][1])
# 焦煤
future_coking = getFutureData(future_path['焦煤'][0], future_path['焦煤'][1])
# 焦炭
future_coal = getFutureData(future_path['焦炭'][0], future_path['焦炭'][1])
# 螺纹钢
future_steel = getFutureData(future_path['螺纹钢'][0], future_path['螺纹钢'][1])

# 现货 --------------------------------------------------------
# 铁矿石
spot_ore = getData(spot_path['铁矿石'][0], spot_path['铁矿石'][1])
# 焦煤
spot_coking = getData(spot_path['焦煤'][0], spot_path['焦煤'][1])
# 焦炭
spot_coal = getData(spot_path['焦炭'][0], spot_path['焦炭'][1])
# 螺纹钢
spot_steel = getData(spot_path['螺纹钢'][0], spot_path['螺纹钢'][1])

# 这个时候就获取到了所有的数据了
# 接下来就要整合所有的数据了
