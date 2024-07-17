import time
import xlwt

from 获取指定日期的星期数 import getSpecificDay, get_next_day
from 将数据进行错开匹配_频率为日 import get_data, get_future_data
from 匹配两个Excel中的数据对 import makeDir

# 创建一个获取给定日期所在周的所有工作日的数据
def get_all_weekday(date):
    """

    :param date: 格式为"2020-01-01"
    :return: 列表，该列表中用于获取date所在周的所有的工作日的日期，元素的格式为"2020-01-01"
    """
    weekday_date_li = []
    li = [0, 1, 2, 3, 4, 5, 6]
    # 格式转换
    date = time.strftime("%Y-%m-%d", time.strptime(date, '%Y-%m-%d'))
    for day in li:
        result = getSpecificDay(date, day)
        weekday_date_li.append(result)

    return weekday_date_li

# 这里的匹配是有问题的，因为没有进行错开匹配，所以是不行的
# 要获取的是前一周的数据

def abbr_to_full(date):
    """

    :param date: 格式为"20200101"
    :return: 格式为"2020-01-01"
    """
    return date[0:4] + '-' + date[4:6] + '-' + date[6:]



# 这种情况下肯定是周数据比较少，这个时候要考虑如何匹配数据
# 暂时先不考虑将周数据充当为日数据，而仅仅是匹配将日数据与所在的周进行匹配
def week_to_day(future_excel, other_excel, f_col, o_col):
    """
    用来匹配周数据的，比如现在有一个周数据，要让它和日数据进行匹配，只要找到一条日数据所在的周是和这条周数据是同一个周就是满足条件的
    :param future_excel: 期货数据Excel文件的所在路径
    :param other_excel: 其他数据（例如：现货）Excel文件所在的路径
    :param f_col: 要获取的期货数据Excel文件中的第几列数据
    :param o_col: 要获取的其他数据（例如：现货）Excel文件中的第几列数据
    :return: 返回值为一个字典，字典的key为日期，格式为"20200101"，键为列表，列表的第一个元素是期货的数据，第二个元素是其他
    Excel文件中的数据
    """
    future_data_dict = get_future_data(future_excel, f_col) # key是格式为"20200101"的日期
    future_data_keys = list(future_data_dict.keys())
    other_data_dict = get_data(other_excel, o_col)
    return_dict = {}
    for day in list(other_data_dict.keys()):
        saturday = getSpecificDay(abbr_to_full(day), 6)
        next_week_monday = get_next_day(saturday)
        # print('saturday', saturday, 'next day', next_week_monday)
        all_weekday = get_all_weekday(next_week_monday) # 为下一周中的所有天
        for each_day in all_weekday:
            temp_li = []
            if each_day.replace('-','') in future_data_keys:
                # 说明这个时候是在期货数据中找到了指定的工作日了
                other_data = other_data_dict[day]
                future_data = future_data_dict[each_day.replace('-', '')]
                temp_li.append(future_data)
                temp_li.append(other_data)
                return_dict[each_day] = temp_li
                break

    return return_dict

# 数据获取到了之后就要进行存储了
def save_data(future_excel, other_excel, f_col, o_col, save_base_path):
    makeDir(save_base_path)
    # 处理一下要保存的文件的名称
    future_filename = future_excel.split('/')[-1].split('.')[0]
    other_filename = other_excel.split('/')[-1].split('.')[0]
    result_dict = week_to_day(future_excel, other_excel, f_col, o_col)
    book = xlwt.Workbook(f'{other_filename}.xls')
    sheet = book.add_sheet('sheet1')
    sheet.write(0, 0, '日期')
    sheet.write(0, 1, '期货价格')
    sheet.write(0, 2, '其他数据')

    i = 0
    for key in list(result_dict.keys()):
        i += 1
        sheet.write(i, 0, key)
        sheet.write(i, 1, result_dict[key][0][0])
        sheet.write(i, 2, result_dict[key][1][0])


    book.save(save_base_path + f'/^{future_filename}_{other_filename}.xls')



future_excel = '~/Desktop/ 小论文/数据/螺纹钢期货-大智慧.xlsx'

base_path = '~/Desktop/ 小论文/数据/将数据错开后进行匹配/开工率/以周（半月）数据为基准'


other_excel = '~/Desktop/ 小论文/数据/开工率/铁矿石_国产矿山开工率.xls'


save_data(future_excel, other_excel, 4, 1, base_path) # 配对成功

# 处理开工率的问题 这样的逻辑应该是没什么问题的，目前先不用考虑太多其他的东西
