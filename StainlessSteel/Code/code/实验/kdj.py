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


def kdj(excel_path, i, j, k, dealing_date, starting_date='2015-09-09'):
    if dealing_date == starting_date:
        k = 50
        d = 50
    data_list = get_data(excel_path)
    dealing_date_index = 0
    for record in data_list:
        if dealing_date == record[0]:
            break
        else:
            dealing_date_index += 1
    starting_date_index = 0
    for record in data_list:
        if starting_date == record[0]:
            break
        else:
            starting_date_index += 1
    tmp_list = data_list[starting_date_index:dealing_date_index]
    k = 0
    d = 0
    j = 0
    rsv = 0
    count = starting_date_index
    for record in tmp_list:
        # rsv的计算
        # Pt Lit Hit Lit
        Pt = record[4]
        L_start_index = count - i
        rsv_tmp_list = data_list[L_start_index:count]
        Lit = rsv_tmp_list[0][3]
        Hit = rsv_tmp_list[0][2]
        for rec in rsv_tmp_list:
            if Lit > rec[3]:
                Lit = rec[3]
            if Hit < rec[2]:
                Hit = rec[2]
        rsv = (Pt - Lit) / (Hit - Lit) * 100  # 把对应的rsv的值给求出来

        if record[0] == starting_date:
            k = 50
            d = 50
        else:
            k = (j - 1) / j * k + 1 / j * rsv
            d = (k - 1) / k * d + 1 / k * k
        j = 3 * d - 2 * k

        count += 1
    return k, d, j

# print(kdj(excel_path, 9, 3, 3, '2015-09-15'))

a = [12,3]
a[1] = 1
print(a)
