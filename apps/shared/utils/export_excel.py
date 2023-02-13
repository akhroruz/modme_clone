import xlwt
from django.http import HttpResponse


# import pandas as pd


def export_data_excel(columns, rows):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

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

# def export_users_to_excel(request):
#     queryset = User.objects.all().values('first_name', 'phone')
#     books_data = list(queryset)
#
#     df = pd.DataFrame(books_data)
#
#     # Write the DataFrame to an Excel file
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="books.xlsx"'
#     df.to_excel(response, index=False)
#     return response
