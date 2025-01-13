# -*- encoding: utf-8 -*-
'''
@File    :   py_xl.py
@Time    :   2025/01/13 12:02:36
@Author  :   Noaghzil
@Version :   1.0
@Contact :   noaghzil@gmail.com
@Last Modified by  :   Noaghzil
@Last Modified time:   2025/01/13 12:02:36
'''

# here put the import lib
import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.worksheet.worksheet import Worksheet

def initialize_worksheet(file_path: str):
    """
    初始化工作表
    """
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    for col in range(1, 12):  # Excel中的A到K列对应的索引是1到11
        for row in range(2, 10001):  # 行号从2到10000
            ws.cell(row=row, column=col).value = ""
    
    add_data_validation(ws, 'G2:G10000', '"男,女"', "请选择正确的性别")
    add_data_validation(ws, 'H2:H10000', '"家庭医生,健康管理师,专科医生"', "请选择正确的角色")
    add_data_validation(ws, 'J2:J10000', '"主任医师,副主任医师,主治医师,住院医师,值班医师,医师,医士,乡村全科助理医师,助理医师,乡村医生,主任药师,副主任药师,主管药师,药师,药士,主任护师,副主任护师,主管护师,护师,护士"', "请选择正确的职称")
    add_data_validation(ws, 'K2:K10000', '"患者可见,患者不可见"', "请选择正确的患者可见状态")
    add_required_validation(ws, 'A2:A10000')
    add_required_validation(ws, 'B2:B10000')
    add_required_validation(ws, 'D2:D10000')
    add_required_validation(ws, 'E2:E10000')
    add_required_validation(ws, 'K2:K10000')
    wb.save('output_data.xlsx')

def add_data_validation(ws: Worksheet, cell_range: str, formula: str, error_message: str):
    """
    添加数据验证
    """
    validation = DataValidation(type="list", formula1=formula, showErrorMessage=True, errorTitle="输入有误", error=error_message, allow_blank=False)
    validation.add(CellRange(cell_range))
    ws.add_data_validation(validation)

def add_required_validation(ws: Worksheet, cell_range: str):
    """
    添加必填项验证
    """
    validation = DataValidation(type="textLength", operator="greaterThan", formula1="0", showErrorMessage=True, errorTitle="必填项缺失", error="此项为必填项，请输入内容", allow_blank=False)
    validation.add(CellRange(cell_range))
    ws.add_data_validation(validation)

# Example usage
if __name__ == "__main__":
    file_path = '/Users/noaghzil/Downloads/医患关系模板.xlsx'
    initialize_worksheet(file_path)