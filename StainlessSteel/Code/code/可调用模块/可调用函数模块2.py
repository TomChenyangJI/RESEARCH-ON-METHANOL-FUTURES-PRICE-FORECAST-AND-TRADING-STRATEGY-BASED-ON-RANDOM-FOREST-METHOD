import os
import time
import datetime

def get_dir(base_path):
    dir_li = os.listdir(base_path)
    result = []
    for ele in dir_li:
        if (os.path.isfile(base_path + '/' + ele)):
            pass
        else:
            result.append(base_path + '/' + ele)
    return result


def get_files(path):
    file_li = os.listdir(path)
    result = []
    for ele in file_li:
        if ele == '.DS_Store':
            pass
        else:
            if (os.path.isfile(path + '/' + ele)):
                result.append(path + '/' + ele)
    return result


def get_next_day(date):
    """
    用来获取指定日期date的后一天的日期
    :param date: 指定的日期，格式为"2020-01-01"
    :return: 返回指定日期的后一天的日期，返回的格式为"2020-01-01"
    """
    delta = datetime.timedelta(-1)
    struct_obj = time.strptime(date, '%Y%m%d')
    datetime_obj = datetime.datetime(struct_obj.tm_year, struct_obj.tm_mon, struct_obj.tm_mday)
    datetime_obj += delta
    return str(datetime_obj.strftime('%Y%m%d'))


def day_match_month_or_week(data1, data2, count):
    """
    此函数是将月数据与天数据进行匹配
    :param data1: 日数据字典
    :param data2: 月数据字典
    :return: 匹配后的字典，key为日期，val为列表，第一个元素是日数据，第二个元素是匹配后的数据
    """
    result = {}
    key_li1 = list(data1.keys())
    key_li2 = list(data2.keys())
    tmp = count

    for key in key_li1:
        count = tmp
        if key in key_li2:
            result[key] = [data1[key], data2[key]]

        else:
            raw_key = key
            while count > 0:
                raw_key = get_next_day(raw_key)
                count -= 1
                if raw_key in key_li2:
                    result[key] = [data1[key], data2[raw_key]]
                    break
    return result
