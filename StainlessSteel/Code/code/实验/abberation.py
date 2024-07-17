import xlrd
import xlwt
import math


def get_data(excel_path):
    # 时间	开	高	低	收	量	额
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    data_list = []
    for row in range(1, rows):
        row_value = []
        # date = xlrd.xldate_as_datetime(sheet.cell_value(row, 0), '').strftime('%Y-%m-%d')
        date = sheet.cell_value(row, 0)
        row_value.append(date)
        for col in range(1, cols):
            val = sheet.cell_value(row, col)
            row_value.append(val)
        data_list.append(row_value)
    return sorted(data_list, key=lambda x : x[0])


# 这里有一个策略 这个策略就是 在取平均值或者标准差的时候
# 到底采用历史数据的值，还是以预测数据的值作为触发
def dispose_average(data_list, length, starting_date, average_col=4):
    # 将指定的平均值添加到行尾
    start_index = 0
    for record in data_list:
        if record[0] == starting_date:
            break
        else:
            start_index += 1
    tag_index = start_index
    for record in data_list[start_index:]:
        # 计算平均值
        sum = 0
        for ele in data_list[(tag_index - length):tag_index]:
            try:
                sum += float(ele[average_col])
            except ValueError:
                break
        ave = sum / length
        # print(record)
        # print(data_list[tag_index])
        record.append(ave)
        data_list[tag_index] = record
        tag_index += 1
    return data_list



def dispose_std(data_list, length, starting_date, std_col=4):
    # 将标准差添加到末尾
    # 同样采用移动标准差
    start_index = 0
    for record in data_list:
        if record[0] == starting_date:
            break
        else:
            start_index += 1
    tag_index = start_index
    for record in data_list[start_index:]:
        # 计算它的标准差
        sqrt_sum = 0
        ave = record[-1]
        for ele in data_list[tag_index-length:tag_index]:
            sqrt_sum += (ele[std_col] - ave)**2
        sqrt_val = math.sqrt(sqrt_sum / length)
        record.append(sqrt_val)

    return data_list


def aveAndSqrt(data_list, length, starting_date, average_col=4, std_col=4):
    data_list = dispose_average(data_list, length, starting_date, average_col)
    data_list = dispose_std(data_list, length, starting_date, std_col)
    return data_list


def disposeBoll(data_list, length, starting_date, k1, k2, average_col=4, std_col=4):
    data_list = aveAndSqrt(data_list, length, starting_date, average_col, std_col)
    tag_index = 0
    for record in data_list:
        if len(record) == 10:
            upper_bound = record[-2] + k1 * record[-1]
            lower_bound = record[-2] - k2 * record[-1]
            record = record[0:9]
            record.append(round(lower_bound, 3))
            record.append(round(upper_bound, 3))
            # print(len(record))
            data_list[tag_index] = record
        tag_index += 1

    return data_list


def wrapper(excel_path, length, starting_date, k1, k2, average_col=4, std_col=4):
    # 时间	开	高	低	收	量	额 移动平均值 布林线下轨 布林线上轨
    # 索引为8的是平均值 9是下轨 10是上轨
    data_list = get_data(excel_path)
    data_list = disposeBoll(data_list, length, starting_date, k1, k2, average_col, std_col)

    return data_list


# 前一天收盘价跌破下轨 第二天开盘就做空
# 出场 当收盘触及到均线的时候就平仓

# 前一天的收盘价突破上轨的时候，第二天就做多
# 出场 当收盘价触及到均线的时候就平仓

# data_list = wrapper(excel_path, 20, '2020-01-02', 1, 1)


# 1为买多 -1为买空 0为平仓 2为不动
def stategy(excel_path, length, starting_date, k1, k2, average_col=4, std_col=4, comparsion_col=4):
    data_list = wrapper(excel_path, length, starting_date, k1, k2, average_col, std_col)
    long_flag = 0
    short_flag = 0
    start_index = 0
    for ele in data_list:
        if ele[0] == starting_date:
            break
        start_index += 1
    tag_index = start_index
    for record in data_list[start_index:len(data_list)-1]:
        # 索引为8的是平均值 9是下轨 10是上轨  11将是tag(表示策略)
        if record[0] == '2021-05-26':
            break
        ave = record[8]
        close = record[comparsion_col]
        upper_bound = record[10]
        lower_bound = record[9]
        tag = 2
        if long_flag == 0 and short_flag == 0:
            if close >= upper_bound:
                long_flag = 1
                tag = 1
            if close <= lower_bound:
                short_flag = 1
                tag = -1
        if long_flag == 1:
            if close <= ave:
                tag = 0
                long_flag = 0

        if short_flag == 1:
            if close >= ave:
                tag = 0
                short_flag = 0
        next_record = data_list[tag_index + 1]
        next_record.append(tag)
        data_list[tag_index + 1] = next_record

        tag_index += 1

    return data_list




def experiment_of_strategy(excel_path, length, starting_date, k1, k2, average_col=4, std_col=4, comparsion_col=4, zero_lower=15, zero_upper=30, one_=5, minus_=5):
    data_list = stategy(excel_path, length, starting_date, k1, k2, average_col, std_col, comparsion_col)
    zero_times = 0
    one_times = 0
    minus_one_times = 0
    for i in data_list:
        if i[-1] == 0:
            zero_times += 1
        if i[-1] == 1:
            one_times += 1
        if i[-1] == -1:
            minus_one_times += 1

    string = f'length is {length}, starting date is {starting_date}, k1 is {k1}, k2 is {k2}\naverage_col is {average_col}, std_col is {std_col}\n'
    string += f"平仓 {zero_times}次， 做多 {one_times}次, 做空 {minus_one_times}次\n"

    # 如果符合条件的话就将数据输出到Excel文件中
    if zero_times >= zero_lower and zero_times <= zero_upper and one_times >= one_ and minus_one_times >= minus_:
        # 进行输出
        # 思考一下输出什么字段
        # 时间 收 预测收盘价 tag
        # 0    4 7        11
        # 保存的名称使用 length k1 k2
        book = xlwt.Workbook()
        sheet = book.add_sheet('sheet01')
        sheet.write(0, 0, '时间')
        sheet.write(0, 1, '收')
        sheet.write(0, 2, '预测收盘价')
        sheet.write(0, 3, 'tag')
        start_index = 0
        for record in data_list:
            if record[0] == starting_date:
                break
            start_index += 1
        end_index = start_index
        for record in data_list[start_index+1:]:
            if record[-1] not in [0, 1, -1, 2]:
                break
            end_index += 1
        row_count = 0
        for record in data_list[start_index+1:end_index]:
            row_count += 1
            sheet.write(row_count, 0, record[0])
            sheet.write(row_count, 1, record[4])
            sheet.write(row_count, 2, record[7])
            sheet.write(row_count, 3, record[11])
        book.save(f'~/Desktop/论文研究/甲醇/交易策略数据/策略实验结果/{length}_{k1}_{k2}.xls')

    return string, zero_times, one_times, minus_one_times


# 接下来的任务是把预测值的数据进行输入

# 实验一 先以历史数据作为计算 平均值 和 标准差 的数据
# 实验一
# if __name__ == '__main__':
#     # --------超参数-----
#     average_col = 4
#     std_col = 4
#     comparsion_col = 4
#     starting_date = '2016-05-11'
#     # --------常量-------
#     excel_path = '~/Desktop/论文研究/甲醇/交易策略数据/策略用.xls'
#     result_file = '策略实验一.txt'
#     file_obj = open(result_file, 'w')
#     print('任务开始')
#     for length in range(5, 60):
#         for tmp_k1 in range(1, 10):
#             k1 = tmp_k1 / 10
#             for tmp_k2 in range(1, 10):
#                 k2 = tmp_k2 / 10
#                 print(length, k1, k2)
#                 string, zero_times, one_times, minus_one_times = experiment_of_strategy(excel_path, length, starting_date, k1, k2, average_col, std_col, comparsion_col)
#                 file_obj.write(string)
#     file_obj.close()
#     print('任务完成')
# 实验而 以预测数据作为计算 平均值 和 标准差 的数据


def experiment(result_file, average_col, std_col, comparsion_col, zero_lower=15, zero_upper=30, one_=5, minus_=5, starting_date='2016-05-11'):
    # --------超参数-----
    average_col = average_col
    std_col = std_col
    comparsion_col = comparsion_col
    starting_date = starting_date
    # --------常量-------
    excel_path = '~/Desktop/论文研究/甲醇/交易策略数据/策略用.xls'
    # result_file = '策略实验一.txt'
    result_file = result_file
    file_obj = open(result_file, 'w')
    print('任务开始')
    for length in range(20, 60):
        print(length)
        for tmp_k1 in range(6, 20):
            k1 = tmp_k1 / 10
            for tmp_k2 in range(6, 20):
                k2 = tmp_k2 / 10
                string, zero_times, one_times, minus_one_times = experiment_of_strategy(excel_path, length, starting_date, k1, k2, average_col, std_col,
                                                comparsion_col, zero_lower, zero_upper, one_, minus_)

                if zero_times >= zero_lower and zero_times <= zero_upper and one_times >= one_ and minus_one_times >=minus_:

                    file_obj.write(string)

    file_obj.close()
    print('任务完成')

# experiment('策略式样一.txt', 4, 4, 4, '2016-05-04')

# import threading
import multiprocessing
#                                                              ave_col  std_col com_col zero_lower zero_upper one_ minus_
t1 = multiprocessing.Process(target=experiment, args=('策略实验一.txt', 4, 4, 7, 10, 20, 5, 5))

# t2 = multiprocessing.Process(target=experiment, args=('策略实验二.txt', 7, 7, 7, '2016-05-04'))

t1.start()
# t2.start()


# 策略已经做好了，接下来要看一下策略的结果是如何的
# -1 是做空 1是做多 0是平仓

import time
time.sleep(2)
import 交易策略实验.处理aberration策略结果

# 实验的结果表明，length k1 k2 的值为 44-48 0.9 0.6 的时候收益应该会达到最大