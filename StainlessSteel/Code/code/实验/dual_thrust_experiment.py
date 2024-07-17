import xlrd
import xlwt

excel_path = '~/Desktop/论文研究/甲醇/甲醇-大智慧.xlsx'


def get_data(excel_path):
    # 时间	开	高	低	收	量	额
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    data_list = []
    for row in range(1, rows):
        row_value = []
        date = xlrd.xldate_as_datetime(sheet.cell_value(row, 0), '').strftime('%Y-%m-%d')
        row_value.append(date)
        for col in range(1, cols):
            val = sheet.cell_value(row, col)
            row_value.append(val)
        data_list.append(row_value)
    return sorted(data_list, key=lambda x : x[0])


# 后面需要做的工作是将收盘价以预测的结果进行替换，然后使用这个模块进行处理
def dualThrust(N, K1, K2, dealing_date, data_list):
    """
    这个函数只需要计算单个交易日的策略值
    可根据返回的结果来判断应该进行多或空操作
    :param N:
    :param K1:
    :param K2:
    :param dealing_date:
    :param data_list:
    :return: 1 0 -1 如果返回1则说明要做多，如果返回0的话说明不需要做任何操作，
    # 如果返回的值为-1则说明要进行做空操作
    """
    Open = 0
    last_close = 0
    count = 0
    for record in data_list:
        if record[0] == dealing_date:
            Open = record[1]
            break
        else:
            count += 1

    # 这个时候说明已经找到了指定的日期，接下来就是要获取响应的数据了
    # 计算HH
    last_close = data_list[count-1][4]
    start_index = count - N
    N_list = data_list[start_index:count]
    HH = 0  # 最高价的最高价
    LC = N_list[0][3]  # 收盘价的最低价
    HC = 0  # 收盘价的最高价
    LL = N_list[0][3]  # 最低价的最低价
    for record in N_list:
        if HH < record[2]:  # 看一下这里有没有计算错误
            HH = record[2]
        if LC > record[4]:
            LC = record[4]
        if HC < record[4]:
            HC = record[4]
        if LL > record[3]:
            LL = record[3]

    Range = max(HH-LC, HC-LL)
    Close = data_list[count - 1][3]
    UpperLine = Close + K1 * Range
    LowerLine = Close - K2 * Range
    # print(K1 * Range, K2 * Range)

    #
    # print(UpperLine, LowerLine, Range, Open)

    # 这里的计算好像出现了点问题，还是要看一下这个到底是怎么回事
    if Open >= UpperLine:
        tag = 1
    if Open <= LowerLine:
        tag = -1
    if Open > LowerLine and Open < UpperLine:
        tag = 0
    return tag


# 接下来的工作是什么

def disposalData(excel_path, N, K1, K2):
    data_list = get_data(excel_path)
    for record in data_list[N:]:
        short_or_long = dualThrust(N, K1, K2, record[0], data_list)
        record.append(short_or_long)
    # 接下来的工作是将结果写入到Excel文件中
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet01')
    # 时间	开	高	低	收	量	额 long_or_short
    title = ['时间', '开', '高', '低', '收', '量', '额', 'long_or_short']
    for i in range(8):
        sheet.write(0, i, title[i])
    row = 0
    for record in data_list:
        row += 1
        for col in range(len(record)):
            sheet.write(row, col, record[col])

    book.save('dual_thrust_disposal.xls')


# disposalData(excel_path, 5, 0.3, 0.5)  # 代码写的好像有点问题，需要看一下


from kdj import kdj
starting_date = '2015-09-09'
# print(kdj(excel_path, 9, 3, 3, '2015-09-15', starting_date=starting_date))

# 接下来的任务是进行策略的执行

def wrapper(excel_path, starting_date, i, j, k, N, k1=0.7, k2=0.7, minus=0.2):
    data_list = get_data(excel_path)
    starting_index = 0
    for record in data_list:
        if record[0] == starting_date:
            break
        else:
            starting_index += 1

    data_list = data_list[starting_index:]
    for record in data_list:
        date = record[0]
        k, d, j = kdj(excel_path, i, j, k, date, starting_date)
        if k > 50 and d > 50 and j > 50:
            k1 -= minus
        if k < 50 and d < 50 and j < 50:
            k2 -= minus
        short_or_long = dualThrust(N, k1, k2, date, get_data(excel_path))
        print(short_or_long)

# wrapper(excel_path, starting_date, 9, 3, 3, 9)
# wrapper(excel_path, starting_date, i=20, j=3, k=3, N=5, k1=0.4, k2=0.4, minus=0.1)
# 这个策略基本上是失败的，除非对dual thrust策略进行修改，这里其实用的已经不是这个策略了
a = [2, 3 ]
a.insert(0, 2)
print(a)