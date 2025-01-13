from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation

# 创建工作簿和工作表
wb = Workbook()
main_ws = wb.active
main_ws.title = "MainSheet"

options_ws = wb.create_sheet(title="OptionsSheet")

# 在 OptionsSheet 中写入选项值
options = [f"Option {i}" for i in range(1, 101)]
for i, value in enumerate(options, start=1):
    options_ws[f"A{i}"] = value

# 定义数据验证，引用 OptionsSheet 的单元格范围
dv = DataValidation(type="list", formula1="'OptionsSheet'!$A$1:$A$100", allow_blank=True)

# 将数据验证添加到 MainSheet 的 B 列（从 B1 到 B1048576，Excel 的最大行数）
main_ws.add_data_validation(dv)
dv.add(f"B1:B1048576")

# 保存文件
wb.save("example_b_column_validation.xlsx")
