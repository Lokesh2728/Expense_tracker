from django import forms
from expenses.models import *

class ExpenseForm(forms.ModelForm):
    class Meta:
        model=Expense
        exclude=['username','date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

