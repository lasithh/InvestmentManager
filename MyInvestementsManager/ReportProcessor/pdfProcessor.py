import PyPDF2
from MyInvestementsManager.models import CompanyFinanceReportSumary


def readPDFFiles() :
    pdfFileObj = open('C:/Work/personal/Annual Reports/Royal Ceremics/2016.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObject = pdfReader.getPage(6)

    text = pageObject.extractText();
    
    #print(text)

    lines = text.splitlines()

    financialSummary = CompanyFinanceReportSumary()
    field = None
    for line in lines :
        if field is not None:
            line.split()
            setattr(financialSummary, field, 999999)
            field = None
        
        if "Turnover - Gross" in line:
            field =  "grossTurnOver"
            continue;        

    attributes = ''
    for field in CompanyFinanceReportSumary._meta.get_fields() :  # @UndefinedVariable :
        attributes += field.name + " = "
        if getattr(financialSummary, field.name, None):
            attributes += str(getattr(financialSummary, field.name))
            
    return attributes