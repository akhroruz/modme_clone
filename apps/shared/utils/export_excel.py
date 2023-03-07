import xlwt
from django.http import HttpResponse



def export_data_excel(columns, rows, file_name: str ='Users'): # noqa
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.xlsx"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(file_name)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response