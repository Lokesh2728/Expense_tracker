from django import forms
from expenses.models import *
from decimal import Decimal




class ExpenseForm(forms.ModelForm):
    class Meta:
        model=Expense
        exclude=['username','date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Pass user from the view
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        budget = Balance.objects.filter(user_id=self.user).first()

        if not budget:
            raise forms.ValidationError("No budget set for this user.")

        if amount > budget.balance:
            raise forms.ValidationError("Insufficient funds for this transaction.")
        return amount

    def clean(self):
        clened_data =  super().clean()
        amount=clened_data['amount']

        try:
            monthly_buget=Buget.objects.get(username=self.user)

            if  Decimal(amount) > monthly_buget.budget:
                raise  forms.ValidationError("You have been  exceed your monthly budget")
        except Buget.DoesNotExist:
            raise forms.ValidationError("monthly budhget not set")



        return



class Budgetform(forms.ModelForm):
    class Meta:
        model=Buget
        fields=['budget']
        widgets={
            'budget':forms.NumberInput(attrs={
                'placeholder': 'Enter your monthly budget'
            })
        }
