import xlrd
import xlwt
import os

# 暂时先匹配两个数据，因为有的数据可能不需要，所以不需要将所有的数据进行匹配
# 相关性分析之后可以匹配所需要的数据

def makeDir(path):
    """

    :param path: 创建文件夹路径
    :return: None
    """
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def getDataPair(excel_obj):
    """

    :param excel_obj: 工作表对象
    :return: 字典数据
    """
    data_dict = {}
    row = excel_obj.nrows

    for i in range(1, row):
        date = str(int(float(excel_obj.cell_value(i, 0))))
        data = excel_obj.cell_value(i, 1)
        data_dict[date] = data
    return data_dict

def getFileName(excel_path):
    """

    :param excel_path: Excel文件的绝对路径
    :return: 去除文件后缀的名称
    """
    result = excel_path.split('/')
    fileNameWithsuffix = result[-1]
    return fileNameWithsuffix.split('.')[0]


def matchFunc(excel1, excel2, prefix):
    """

    :param excel1: 第一个Excel文件的路径 也就是期货的数据
    :param excel2: 第二个Excel文件的路径
    :param prefix: 用于添加到保存文件名称的前缀
    :return:
    """
    # 出现的相同的数据的时候怎么办 输出到一个文件中 把期货的数据放在第一列，其他数据放在第二列
    excel_obj1 = xlrd.open_workbook(excel1).sheet_by_index(0)
    excel_obj2 = xlrd.open_workbook(excel2).sheet_by_index(0)

    row1 = excel_obj1.nrows
    row2 = excel_obj2.nrows

    file_name1 = getFileName(excel1)
    file_name2 = getFileName(excel2)

    excel_data1 = getDataPair(excel_obj1)
    excel_data2 = getDataPair(excel_obj2)
    # common_file = open(f'../匹配Excel文件的输出结果文件/{prefix}' + file_name1 + '_' + file_name2 + '.txt', 'w')
    # first_different_file = open(f'../匹配Excel文件的输出结果文件/{prefix}不同_' + file_name1 + '.txt', 'w')
    # second_different_file = open(f'../匹配Excel文件的输出结果文件/{prefix}不同_' + file_name2 + '.txt', 'w')
    makeDir(f'~/Desktop/ 小论文/数据/Excel匹配数据/{prefix}')
    common_file = xlwt.Workbook(f'~/Desktop/ 小论文/数据/Excel匹配数据/{prefix}/{prefix}_' + file_name1 + '_' + file_name2 + '.xls')
    common_sheet = common_file.add_sheet('sheet1')
    common_sheet.write(0, 0, '日期')
    common_sheet.write(0, 1, '期货价格')
    common_sheet.write(0, 2, '数据')

    first_file = xlwt.Workbook(f'~/Desktop/ 小论文/数据/Excel匹配数据/{prefix}/{prefix}_不同_' + file_name1 + '.xls')
    first_sheet = first_file.add_sheet('sheet1')
    first_sheet.write(0, 0, '日期')
    first_sheet.write(0, 1, '期货价格')

    second_file = xlwt.Workbook(f'~/Desktop/ 小论文/数据/Excel匹配数据/{prefix}/{prefix}_不同_' + file_name2 + '.xls')
    second_sheet = second_file.add_sheet('sheet1')
    second_sheet.write(0, 0, '日期')
    second_sheet.write(0, 1, '数据')

    common_date = []
    if row1 >= row2:
        # 对row1进行遍历
        i = 0
        for date in list(excel_data1.keys()):
            if date in list(excel_data2.keys()):
                i += 1
                # 说明这条数据是两者都有的
                record_tup = (date, excel_data1[date], excel_data2[date])
                # 进行输入工作
                common_sheet.write(i, 0, record_tup[0])
                common_sheet.write(i, 1, float(record_tup[1]))
                common_sheet.write(i, 2, float(record_tup[2]))

                common_date.append(date)

    else:
        # 对row2进行遍历
        i = 0
        for date in list(excel_data2.keys()):

            if date in list(excel_data1.keys()):
                i += 1
                record_tup = (date, excel_data1[date], excel_data2[date])
                common_sheet.write(i, 0, record_tup[0])
                common_sheet.write(i, 1, float(record_tup[1]))
                common_sheet.write(i, 2, float(record_tup[2]))

                common_date.append(date)

    for date in common_date:  # 没有被弹出的就是他们个各自的差集，要写入到各自的文件中
        excel_data1.pop(date)
        excel_data2.pop(date)
    i = 0
    for key in excel_data1.keys():
        i += 1
        first_sheet.write(i, 0, key)
        first_sheet.write(i, 1, float(excel_data1[key]))

    i = 0
    for key in excel_data2.keys():
        i += 1
        second_sheet.write(i, 0, key)
        second_sheet.write(i, 1, float(excel_data2[key]))

    common_file.save(f'~/Desktop/ 小论文/数据/Excel匹配数据/{prefix}/{prefix}_' + file_name1 + '_' + file_name2 + '.xls')
    first_file.save(f'~/Desktop/ 小论文/数据/Excel匹配数据/{prefix}/{prefix}_不同_' + file_name1 + '.xls')
    second_file.save(f'~/Desktop/ 小论文/数据/Excel匹配数据/{prefix}/{prefix}_不同_' + file_name2 + '.xls')


# 螺纹钢的期货价格是一直不变的
# excel_path1 = '~/Desktop/ 小论文/数据/期货数据/红期_螺纹钢期货-主力合约.xlsx'
#
#
# excel_path2 = '~/Desktop/ 小论文/数据/现货数据/螺纹钢.xls'
#
# matchFunc(excel_path1, excel_path2, '螺纹钢现货')
