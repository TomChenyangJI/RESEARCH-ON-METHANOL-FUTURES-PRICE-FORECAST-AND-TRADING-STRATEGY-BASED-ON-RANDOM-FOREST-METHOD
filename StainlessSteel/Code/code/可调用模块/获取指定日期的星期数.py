import datetime
import time

# result = time.strftime('%W')


def getWeekday(format_date):
    """
    此函数用来获取指定日期的time_struct对象
    :param format_date: 格式化的日期，格式为'%Y-%m-%d'
    :return: 返回这个日期是这周中的周几
    """
    result = time.strptime(format_date, '%Y-%m-%d')
    weekday = time.strftime('%w', result)
    return int(weekday)



def getWeekNum(struct_time, date = None): # 这个函数写的好像有问题，要重新写一下
    """
    此函数用来获取指定日期在一年中的第几周
    起始索引是0
    :param struct_time: 时间数组
    :param date: 传入的日期，格式为'%Y-%m-%d'
    :return: 返回指定日期的星期数
    """

    if date != None:
        return time.strftime('%W', time.strptime(date, '%Y-%m-%d'))

    result = time.strftime('%W', struct_time)

    return result


def getSpecificDay(date, weekday):
    """
    该函数用来获取指定日期所在周中的某一天的日期
    注意：0代表的时候星期一，1代表的是星期二，以此类推
    :param date: 指定的日期 格式为'2021-08-01'
    :param weekday: 要获取的同周中的某天
    :return: 返回要获取同周中的某天的日期
    """

    if getWeekday(date) == weekday:
        return date
    else:
        # 要进行转化
        delta = datetime.timedelta(-1)
        while getWeekday(date) != weekday:
            if getWeekday(date) < weekday:
                strp = time.strptime(date, '%Y-%m-%d')
                datetime_obj = datetime.datetime(strp.tm_year, strp.tm_mon, strp.tm_mday)
                datetime_obj = datetime_obj - delta
                date = datetime_obj.strftime('%Y-%m-%d')

            else:
                strp = time.strptime(date, '%Y-%m-%d')
                datetime_obj = datetime.datetime(strp.tm_year, strp.tm_mon, strp.tm_mday)
                datetime_obj = datetime_obj + delta
                date = datetime_obj.strftime('%Y-%m-%d')
        return date



# des = '2021-05-20'
# result = getSpecificDay(des, 0)
# print(result)

# 获取前一天的数据，如果今天是周一的话，那么就要获取上周五的时间
def get_yesterday(date):
    """
    用来获取date这一天的前一天的日期
    :param date: 格式为"20200101"，或者"2020-01-01"
    :return: 返回这一天的前一天的日期，格式为"2020-01-01"
    """
    tem = 0
    if '-' not in date:
        tem = time.strptime(date, "%Y%m%d")
    elif '-' in date:
        tem = time.strptime(date, "%Y-%m-%d")
    # format_date = time.strftime("%Y-%m-%d", tem)
    delta = datetime.timedelta(-1)
    datetime_obj = datetime.datetime(tem.tm_year, tem.tm_mon, tem.tm_mday)
    datetime_obj = datetime_obj + delta
    return datetime_obj.strftime("%Y%m%d")

def get_next_day(date):
    """
    用来获取指定日期date的后一天的日期
    :param date: 指定的日期，格式为"2020-01-01"
    :return: 返回指定日期的后一天的日期，返回的格式为"2020-01-01"
    """
    delta = datetime.timedelta(1)
    time_struct = time.strptime(date, '%Y-%m-%d')
    result = datetime.datetime(time_struct.tm_year, time_struct.tm_mon, time_struct.tm_mday) + delta
    return result.strftime("%Y-%m-%d")

# test
# dday = '2020-05-17'
# # result = getWeekday(dday)
# print(getSpecificDay(dday, 6))