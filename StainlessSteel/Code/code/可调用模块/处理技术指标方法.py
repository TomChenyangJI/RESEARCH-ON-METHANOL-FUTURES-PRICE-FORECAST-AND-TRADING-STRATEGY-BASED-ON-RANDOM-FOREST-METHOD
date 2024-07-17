import xlrd
import xlwt
import sys
sys.setrecursionlimit(2000) # 用来设置递归的深度的，我这里设置的递归神队为2000此递归


def getData(excel_path, col):
    """
    此函数用来获取指定的Excel文件中的指定col列的数据
    :param excel_path: Excel文件所在的位置
    :param col: 所要获取的数据所在的列
    :return: 返回值为字典，key为日期，格式为"20200520"，value为col列的值
    """
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(0)
    result = {}
    rows = sheet.nrows
    for i in range(1, rows):
        ddate = sheet.cell_value(i, 0)
        ddate = xlrd.xldate_as_datetime(ddate,'').strftime('%Y%m%d')
        val = sheet.cell_value(i, col)
        result[ddate] = val
    return result

# 这里的技术指标是将Excel文件中的数据规范化之后进行的处理，
# 否则还要进行检查
def getPSY(excel_path, col, amount, start_date): # 这个函数已经实现，但是还没有进行检测，还是要检测一下
    # 已经测试过，没有问题
    """
    用于获取指定Excel文件中数据的PSY指标
    :param excel_path: Excel文件所在的位置
    :param col: 所要获取的数据所在的列
    :param amount: 计算PSY指标的时候，采用的周期
    :param start_date: 从那一天开始计算PSY技术指标，比如"20150105"
    :return:
    """
    # 获取Excel文件中的数据
    data = getData(excel_path, col)
    li = list(data.keys())
    start_index = li.index(start_date)
    first_index = start_index - amount
    result = {}
    # 接下来用来获取psy指标
    rows = len(li) + 1
    for i in range(start_index, rows - 1):
        # 对于每一天的数据，计算其psy i
        amount_before_index = i - amount
        count = 0
        for j in range(amount_before_index, i):
            temp = data[li[j]] # val
            before = data[li[j - 1]]
            if temp > before:
                count += 1
        psy = count / amount * 100
        result[li[i]] = round(psy, 2)

    return result


def getOBV(excel_path, col_price, col_amount, amount, start_date):
    """
    用来获取商品的OBV技术指标
    :param excel_path: excel文件所在路径
    :param col_price: 收盘价所在的列
    :param col_amount: 交易量所在的列
    :param amount:
    :param start_date: 从哪一天的数据开始要
    :return: 返回一个字典，key为日期，格式为："20150105"，value为obv值
    """
    price_data = getData(excel_path, col_price)
    amount_data = getData(excel_path, col_amount)
    li = list(price_data.keys())
    start_index = li.index(start_date)
    result = {}
    for inx in range(start_index, len(li)):
        if inx == start_index:
            obv = amount_data[li[inx]]
            result[li[inx]] = obv
        else:
            prev_price = price_data[li[inx - 1]]
            pres_price = price_data[li[inx]]
            if pres_price < prev_price:
                obv = result[li[inx - 1]] - amount_data[li[inx]]
                result[li[inx]] = obv
            elif pres_price > prev_price:
                obv = result[li[inx - 1]] + amount_data[li[inx]]
                result[li[inx]] = obv
            else:
                obv = result[li[inx - 1]]
                result[li[inx]] = obv

    return result



def getWR(excel_path, col, amount, start_date): # 这个函数还没有检验结果的正确性
    """
    用来获取WR值
    :param excel_path: Excel文件所在的位置
    :param col: 所要获取数据在的列数
    :param amount: 向前推算多长时间
    :param start_date: 从哪个时间点是需要的
    :return:
    """
    data = getData(excel_path, col)
    li = list(data.keys())
    inx = li.index(start_date)
    result = {}
    for i in range(inx, len(li)):
        maxVal = data[li[i]]
        minVal = data[li[i]]
        for j in range(i - amount, i):
            val = data[li[j]]
            if val > maxVal:
                maxVal = val
            if val < minVal:
                minVal = val
        try:
            wr = (maxVal - data[li[i]]) / (maxVal - minVal) * 100
            result[li[i]] = round(wr, 2)
        except:
            print('有除数为0的错误')

    return result


def getRSI(excel_path, col, amount, start_date): # 这个函数也没有检测
    """
    用来获取RSI值
    :param excel_path: Excel文件所在的位置
    :param col: 所要获取数据在的列数
    :param amount: 向前推算多长时间
    :param start_date: 从哪个时间点是需要的
    :return:
    """
    data = getData(excel_path, col)
    li = list(data.keys())
    start_index = li.index(start_date)
    result = {}
    for i in range(start_index, len(li)):
        positive = 0
        negative = 0
        for j in range(i - amount, i):
            former_date = li[j - 1]
            present_date = li[j]
            former_data = data[former_date]
            present_data = data[present_date]
            if former_data > present_data:
                negative += (former_data - present_data)
            else:
                positive += (present_data - former_data)
        rsi = positive / (positive + negative) * 100
        result[li[i]] = round(rsi, 2)

    return result

def getRSV(excel_path, col, amount, start_date): # 这个函数还没有检验
    """
        用来获取RSV值
        :param excel_path: Excel文件所在的位置
        :param col: 所要获取数据在的列数
        :param amount: 向前推算多长时间
        :param start_date: 从哪个时间点是需要的
        :return:
    """
    data = getData(excel_path, col)
    li = list(data.keys())
    start_index = li.index(start_date)
    result = {}
    for i in range(start_index, len(li)):
        maxVal = data[li[i]]
        minVal = data[li[i]]
        for j in range(i - amount, i):
            if data[li[j]] > maxVal:
                maxVal = data[li[j]]
            if data[li[j]] < minVal:
                minVal = data[li[j]]
        present_data = data[li[i]]
        rsv = (present_data - minVal) / (maxVal - minVal) * 100
        result[li[i]] = round(rsv, 2)

    return result

def getKDJ(excel_path, col, amount, start_date, k_i, d_i): # 此函数没有进行检验
    """
        :param excel_path: Excel文件所在的位置
        :param col: 所要获取数据在的列数
        :param amount: 向前推算多长时间
        :param start_date: 从哪个时间点是需要的
        :param k_i: k值计算向前推算的时间
        :param d_i: d值计算向前推算的时间
        :return: 返回值为一个字典，key为日期，val为数组（k，d，j）
    """
    result = {} # key是日期，val为数组（k，d，j）
    k = {}
    d = {}
    j = {}
    rsv = getRSV(excel_path, col, amount, start_date)
    li = list(rsv.keys())
    size = len(list(rsv.keys()))
    present_rsv = rsv[start_date]
    k[start_date] = 50
    kt_1 = list(k.keys())[-1]
    d[start_date] = 50
    k[kt_1] * (k_i - 1) / k_i + 1 / k_i * present_rsv
    for i in range(1, size): # 此循环用来计算k值
        # i 代表的是每一个交易日
        present_rsv = rsv[li[i]]
        previous_date = li[li.index(li[i]) - 1]
        kt_1 = k[previous_date]# 为前一天的k值
        kt = (k_i - 1) / k_i * kt_1 + 1 / k_i * present_rsv
        k[li[i]] = round(kt, 2)
    for i in range(1, size): # 此循环用来计算d值
        kt = k[li[i]]
        previous_date = li[li.index(li[i]) - 1]
        dt_1 = d[previous_date]# 用来获取前一天的d值
        dt = (d_i - 1) / d_i * dt_1 + 1 / k_i * kt
        d[li[i]] = round(dt, 2)
    for i in range(1, size):
        jt = 3 * d[li[i]] - 2 * k[li[i]]
        j[li[i]] = round(jt, 2)
    for i in range(1, size):
        result[li[i]] = (k[li[i]], d[li[i]], j[li[i]])

    return result


def getY(data, N, mark_date, present_date, distance): # 这里的递归写的有问题，看哪里出现问题了
    # 主要是要确定递归的次数
    """
    用于获取EMA，指数移动平均值
    是使用起始点的日期所对应的数据来替代EMA1的
    :param data: 字典数据
    :param N:
    :param start_date: 从哪一天的数据开始要
    :param distance: 这里的distance是指目前的日期，present_date距离mark_date的距离
    :return: 为一个字典，其key为日期，值为该日期相对于mark_date对应的EMA值
    """
    li = list(data.keys())
    if distance == 0:
        X = data[mark_date]
        return X
    else:
        present_index = li.index(present_date)
        previous_date = li[present_index - 1]
        X = data[present_date]
        Y = (2 * X + (N - 1) *getY(data, N, mark_date, previous_date, distance - 1)) / (N + 1)
        return Y

def getMACD(excel_path, col, amount, mark_date, i, j, k):
    """
    用于获取Excel文件中的MACD数据
    :param excel_path: Excel文件所在的位置
    :param col: 所要获取数据在的列数
    :param amount: 向前推算多长时间
    :param mark_date: 要从哪一天的数据开始要
    :param i: 计算EMA（i）使用
    :param j: 计算EMA（j）使用
    :param k: 计算dea使用
    :return: 为一个数组，其中的每一个元素都是字典，其中元素为EMA（i），EMA（j），dif，dea
    """
    # EMA 的计算
    result = []
    data = getData(excel_path, col)
    li = list(data.keys())
    start_index = li.index(mark_date)
    ema_i = {}
    ema_j = {}
    dif = {}
    dea = {}
    for inx in range(start_index, len(li)):
        # print(inx, '----')
        distance = inx - start_index # 距离的计算有没有出错
        emaVal = getY(data, i, mark_date, li[inx], distance)
        ema_i[li[inx]] = round(emaVal, 2)
    for inx in range(start_index, len(li)):
        # print(inx, '****')
        distance = inx - start_index
        emaVal = getY(data, j, mark_date, li[inx], distance)
        ema_j[li[inx]] = round(emaVal, 2)
    for key in list(ema_i.keys()):
        difVal = ema_i[key] - ema_j[key]
        dif[key] = round(difVal, 2)
    dea[mark_date] = dif[mark_date]
    for i in range(start_index + 1, len(li)):
        deaVal = (k - 1) / (k + 1) * dea[li[i - 1]] + 2 / (k + 1) * dif[li[i]]
        dea[li[i]] = round(deaVal, 2)
    result.append(ema_i)
    result.append(ema_j)
    result.append(dif)
    result.append(dea)
    return result


# test
excel_path = '~/Desktop/ 小论文/数据/螺纹钢期货-大智慧.xlsx'
# result = getData(excel_path, 1)
# r = getPSY(excel_path, 4, 8, '20150105')
# print(r)
# result = getOBV(excel_path)
# print(result)
# r = getWR(excel_path, 4, 8, '20150105')
# print(r)

# result = getRSI(excel_path, 4, 8, '20150105')
# print(result)

# result = getKDJ(excel_path, 4, 8, '20150105', 9, 5)
# print(result)

# result = getMACD(excel_path, 4, 8, '20150105', 8, 9, 8)

def saveMACDDataToExcel(excel_path, col, amount, mark_date, i, j, k, save_path, save_name):
    ema_i, ema_j, dif, dea = getMACD(excel_path, col, amount, mark_date, i, j, k)
    book = xlwt.Workbook(f'{save_path}/{save_name}_{i}_{j}_{k}.xls')
    sheet = book.add_sheet('sheet01')
    # 接下来就是数据的写入操作
    # 先写入第一行的行标题
    sheet.write(0, 0, '日期')
    sheet.write(0, 1, 'ema_' + str(i))
    sheet.write(0, 2, 'ema_' + str(j))
    sheet.write(0, 3, 'dif')
    sheet.write(0, 4, 'dea')
    # 开始写入数据
    count = 1
    for key in list(ema_i.keys()):
        emaiVal = ema_i[key]
        emajVal = ema_j[key]
        difVal = dif[key]
        deaVal = dea[key]
        sheet.write(count, 0, key)
        sheet.write(count, 1, emaiVal)
        sheet.write(count, 2, emajVal)
        sheet.write(count, 3, difVal)
        sheet.write(count, 4, deaVal)
        count += 1
    book.save(f'{save_path}/{save_name}_{i}_{j}_{k}.xls')

# saveMACDDataToExcel(excel_path, 4, 8, '20150105', 8, 9, 8, './', 'MACD')

def saveDictDataToExcel(data_dict, save_path, save_name):
    # 这个函数目前还没有想好这个函数的用途，暂时可以先不写
    pass

# result = getOBV(excel_path, 4, 5, 14, '20150105')


# excel_path = '~/Desktop/ 小论文/数据/螺纹钢期货-大智慧.xlsx'
#
# print(result)
# macd = getMACD(excel_path, 4, 14, '20150105', 9, 3, 3)
# print(macd)
