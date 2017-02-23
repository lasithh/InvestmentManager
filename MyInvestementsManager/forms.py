from django import forms
from MyInvestementsManager.models import CompanyFinanceReportSumary

class CompanyFinanceReportSumaryForm(forms.ModelForm):
    class Meta:
        model = CompanyFinanceReportSumary
        fields = [ 'company', 'revenue', 'profitBeforeTax', 'profitAfterTax', 'grossDividends', 'interestCover', 'currentRatio', 'issueDate', 'description', 'totalAssets', 'totalShareHolderFunds', 'numberOfShares',  'currency' ]

        widgets = {
            'issueDate': forms.DateInput(attrs={'class':'datepicker'}),
            }
        