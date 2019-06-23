import traceback

import pyPdf
from tabula import read_pdf


def extract_tables(file_path):
    output = dict()
    fh = open(file_path, mode='rb')
    reader = pyPdf.PdfFileReader(fh)
    n = reader.getNumPages()
    fh.close()
    for i in range(n):
        try:
            df = read_pdf(file_path, pages=str(i + 1), multiple_tables=True)
        except Exception as e:
            print("Ignored error occured during tables extraction")
            print traceback.format_exc()

        if df:
            list_of_tables = list()
            for df_table in df:
                list_of_tables.append(df_table.to_json())
            output[i] = list_of_tables


    return output
