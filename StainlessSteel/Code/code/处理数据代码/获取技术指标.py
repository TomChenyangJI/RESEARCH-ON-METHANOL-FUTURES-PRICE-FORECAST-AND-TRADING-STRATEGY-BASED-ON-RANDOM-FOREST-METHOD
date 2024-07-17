import 处理技术指标方法 as dis


excel_path = '~/Desktop/论文研究/甲醇/甲醇-大智慧.xlsx'

obv = dis.getOBV(excel_path, 4, 5, 14, '20140618')
kdj = dis.getKDJ(excel_path, 4, 14, '20140618', 3, 3)
rsi = dis.getRSI(excel_path, 4, 14, '20140618')
wr = dis.getWR(excel_path, 4, 14, '20140618')
psy = dis.getPSY(excel_path, 4, 14, '20140618')
# macd需要特殊处理，因为它的返回值太特殊
# macd = dis.getMACD(excel_path, 4, 14, '20140102', 9, 3, 3)

# print(macd)



def matchData(data, name):
    """
    将字典data中的数据添加到字典中original_dict
    :param original_dict: 是一个字典，key是日期，格式为'20210524'，val是列表，格式为列表[, , , ...]，列表中的元素是一个特征值
    :param data: 是一个特征数据集，其格式为字典，该字典的key为日期，格式为'20210524'，val是值
    :param name: 要添加的特征值的名称
    :return: 将新特征添加到original_dict之后返回
    """
    global head  # head: 用来记录目前original_dict中的val列表中数据对应的特征名称
    global original_dict # original_dict: 是一个字典，key是日期，格式为'20210524'，val是列表，格式为列表[, , , ...]，列表中的元素是一个特征值 # {'20210524':[, , , ...]}
    data_keys = list(data.keys())
    head.append(name)
    for key in list(original_dict.keys()):
        if key in data_keys:
            original_dict[key].append(data[key])
        else:
            original_dict.pop(key)


from 可调用函数模块 import getData
future_path = '~/Desktop/论文研究/甲醇/甲醇期货价格.xls'
future_data = getData(future_path, 1)
head = []
original_dict = {}
head = ['甲醇期货价格']
for key in list(future_data.keys()):
   original_dict[key] = [future_data[key]]
matchData(obv, 'obv')
matchData(rsi, 'rsi')
matchData(wr, 'wr')
matchData(psy, 'psy')
# matchData(macd, 'macd')
# macd需要特殊处理，因为返回值太复杂了


# 处理kdj
# 只需要用j指标即可
kdj_dispose = {}
for key in list(kdj.keys()):
    kdj_dispose[key] = kdj[key][-1]
matchData(kdj_dispose, 'kdj')

# 处理macd
macd = dis.getMACD(excel_path, 1, 14, '20140618', 9, 3, 3)
macd_dea = macd[-1]

matchData(macd_dea, 'macd_dea')
print(head)
print(original_dict)



import xlwt

book = xlwt.Workbook()
sheet = book.add_sheet('sheet01')
sheet.write(0, 0, '日期')
# sheet.write(0, 1, head[0])
# sheet.write(0, 2, head[1])
# sheet.write(0, 3, head[2])
# sheet.write(0, 4, head[3])
# sheet.write(0, 5, head[4])
for i in range(len(head)):
    sheet.write(0, i + 1, head[i])
length = len(head)
i = 0
for key in list(original_dict.keys()):
    i += 1
    sheet.write(i, 0, key)
    for size in range(length):
        sheet.write(i, size + 1, original_dict[key][size])
    # sheet.write(i, 1, original_dict[key][0])
    # sheet.write(i, 2, original_dict[key][1])
    # sheet.write(i, 3, original_dict[key][2])
    # sheet.write(i, 4, original_dict[key][3])
    # sheet.write(i, 5, original_dict[key][4])
book.save('~/Desktop/论文研究/甲醇/技术指标数据.xls')
