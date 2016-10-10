import PyPDF2
from MyInvestementsManager.models import CompanyFinanceReportSumary

pdfFileObj = open('C:/Work/personal/Annual Reports/Royal Ceremics/2016.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObject = pdfReader.getPage(6)

text = pageObject.extractText();

lines = text.splitlines()

financialSummary = CompanyFinanceReportSumary()
field = None
for line in lines :
    if field is not None:
        setattr(financialSummary, field, 100)
        field = None
        
    if line.contains("Turnover - Gross"):
        field =  "grossTurnOver"
        break;
        


for fieldName in CompanyFinanceReportSumary._meta.get_all_field_names() :  # @UndefinedVariable :
    print(fieldName)
            
