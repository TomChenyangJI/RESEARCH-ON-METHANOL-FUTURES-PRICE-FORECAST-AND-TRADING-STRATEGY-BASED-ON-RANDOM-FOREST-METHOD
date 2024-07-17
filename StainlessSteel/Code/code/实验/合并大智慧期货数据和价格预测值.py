import xlrd
import xlwt
import time

predict_path = '~/Desktop/论文研究/甲醇/交易策略数据/期货价格预测值.xls'
dazhihui_path = '~/Desktop/论文研究/甲醇/甲醇-大智慧.xlsx'


def get_excel_data(excel_path):
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(0)
    da_rows = sheet.nrows
    da_col = sheet.ncols
    da_data = []
    for i in range(1, da_rows):
        try:
            tmp = [xlrd.xldate_as_datetime(sheet.cell_value(i, 0), '').strftime('%Y-%m-%d')]
        except OverflowError:
            tmp = [time.strftime('%Y-%m-%d', time.strptime(str(int(sheet.cell_value(i, 0))), '%Y%m%d'))]
        for col in range(1, da_col):
            val = sheet.cell_value(i, col)
            tmp.append(val)
        da_data.append(tmp)
    return da_data


def output_to_excel(dazhihui_path, predict_path):
    dazhihui_data = get_excel_data(dazhihui_path)
    predict_data = get_excel_data(predict_path)

    # 获取到数据之后下一步骤就是要进行数据拼凑，然后写入到文件中
    tmp = {i[0]:i[1] for i in predict_data}

    count_tag = 0
    for record in dazhihui_data:
        date = record[0]
        if date in tmp.keys():
            record.append(tmp[date])
        count_tag += 1

    # 进行数据的写入操作
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet01')
    # 时间	开	高	低	收	量	额
    title = ['时间', '开', '高', '低', '收', '量', '额', '预测收盘价']
    for i in range(len(title)):
        sheet.write(0, i, title[i])

    count_tag = 1
    for record in dazhihui_data:
        for col in range(len(record)):
            sheet.write(count_tag, col, record[col])
        count_tag += 1
    book.save('~/Desktop/论文研究/甲醇/交易策略数据/策略用.xls')

output_to_excel(dazhihui_path, predict_path)
# 这里为什么会出现缺失值呢？
# 答：出现确实值的原因是合并数据的时候某些日期的样本是没有的
