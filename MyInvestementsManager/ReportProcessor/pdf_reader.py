import pyPdf
from tabula import read_pdf


def extract_tables(file_path):
    output = dict()
    fh = open(file_path, mode='rb')
    reader = pyPdf.PdfFileReader(fh)
    n = reader.getNumPages()
    fh.close()
    for i in range(n):
        df = read_pdf(file_path, pages=str(i + 1), multiple_tables=True)
        if df:
            output[i] = df

    return output
