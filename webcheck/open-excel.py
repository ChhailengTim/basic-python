import pandas as pd

data = pd.ExcelFile(r'E:\CHHAILENG\basic-python\webcheck\customer_list.xlsx')
print(data.sheet_names)

import xlrd

loc = r"E:\CHHAILENG\basic-python\webcheck\customer_list.xlsx"
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

print(sheet.cell_value(0, 0))
