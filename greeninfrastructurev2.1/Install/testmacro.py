from openpyxl import load_workbook
import openpyxl

print openpyxl.__version__
fileName = r"P:\Misc Projects\Grey_to_GreenInfrastructure\Python Tool\greeninfrastructurev2\Install\buttons.xlsm"
fileNameOut = r"P:\Misc Projects\Grey_to_GreenInfrastructure\Python Tool\greeninfrastructurev2\Install\outtest.xlsm"
wb = load_workbook(fileName,keep_vba=True,data_only=True)
ws = wb['Sheet1']
wb.save(fileNameOut)

