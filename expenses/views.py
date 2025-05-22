from django.shortcuts import render
from django.views.generic import  CreateView,ListView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from expenses.models import *
from expenses.forms import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from .charts import *

from itertools import chain
from django.utils import timezone



# Create your views here.
def home(request):
    user = request.user  
    monthly_expense=Expense.objects.filter(username=user).aggregate(Sum('amount'))['amount__sum'] or 0 
    recent_transactions = Expense.objects.filter(username=user).order_by('-id')[:3]
    balance = Balance.objects.filter(user_id=request.user).last()
    montly_budget=Buget.objects.filter(username=user).first()
    d = {
        'recent_transactions': recent_transactions,
        'balance':balance,
        'monthly_expense':monthly_expense,
        'montly_budget':montly_budget,
    }
    return render(request, 'home.html', d)



@login_required
def dashboard(request):
    user=request.user
    daily_Expense(user)
    context={
        'bar_chart': 'expenses/static/charts/bar_chart.png'
    }
    return render(request,'dashboard.html')








class AddExpense(LoginRequiredMixin,CreateView):
    model=Expense
    form_class = ExpenseForm
    template_name='AddExpense.html'
    success_url=reverse_lazy('home')


    def form_valid(self, form):
        user = self.request.user
        form.instance.username = user
        new_amount = form.cleaned_data['amount']

        # Get latest total_balance
        latest_balance = Balance.objects.filter(user_id=user).order_by('-created_at', '-time').first()
        previous_total = latest_balance.total_balance if latest_balance else 0

        # Create new Balance entry with Debit
        Balance.objects.create(
            user_id=user,
            Transactin_type='Debit',
            balance=new_amount,
            total_balance=previous_total - new_amount
        )

        # Deduct from monthly budget
        monthly_limit = Buget.objects.get_or_create(username=user)[0]
        monthly_limit.budget -= new_amount
        monthly_limit.save()

        return super().form_valid(form)



class ExpenseList(LoginRequiredMixin,ListView):
    model=Expense
    template_name='ExpenseList.html'
    context_object_name='transactions'

    def get_queryset(self):
        user = self.request.user

        expenses = Expense.objects.filter(username=user).annotate(
            transaction_type=models.Value('Debit', output_field=models.CharField()),
            transaction_amount=models.F('amount'),
            transaction_date=models.F('date'),
            transaction_time=models.Value(None, output_field=models.TimeField())
        )

        balances = Balance.objects.filter(user_id=user).annotate(
            transaction_type=models.F('Transactin_type'),
            transaction_amount=models.F('balance'),
            transaction_date=models.F('created_at'),
            transaction_time=models.F('time')
        )

        combined = sorted(
            chain(expenses, balances),
            key=lambda obj: (obj.transaction_date, obj.transaction_time or timezone.datetime.min.time()),
            reverse=True
        )

        for obj in combined:
            if isinstance(obj, Expense):
                obj.txn_type = 'Expense'
            else:
                obj.txn_type = 'Balance'


        return combined


class Expense_Update(LoginRequiredMixin,UpdateView):
    model=Expense
    form_class=ExpenseForm
    template_name='AddExpense.html'
    success_url = reverse_lazy('ExpenseList')



class Expense_Delete(LoginRequiredMixin,DeleteView):
    model=Expense
    template_name='Expense_delete.html'
    context_object_name='expense'
    success_url=reverse_lazy('home')


class Balanceview(LoginRequiredMixin, CreateView):
    
    model = Balance
    fields = ['balance']
    template_name = 'balance_create.html'
    context_object_name='Balance'
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        user = self.request.user
        form.instance.user_id = user
        form.instance.Transactin_type = 'Credit'
        new_amount = form.cleaned_data['balance']
        # Fetch the latest total_balance
        latest_record = Balance.objects.filter(user_id=user).order_by('-created_at', '-time').first()
        previous_total = latest_record.total_balance if latest_record else 0
        # Update the new total_balance
        form.instance.total_balance = previous_total + new_amount

        return super().form_valid(form)




@login_required
def set_budget(request):
    EBFO = Budgetform()
    d = {'EBFO': EBFO}

    if request.method == 'POST':
        BFO = Budgetform(request.POST)
        if BFO.is_valid():
            budget = BFO.cleaned_data.get('budget')
            budget_obj, created = Buget.objects.get_or_create(username=request.user)
            budget_obj.budget = budget
            budget_obj.save()
            return HttpResponse('created')
        else:
            return HttpResponse('invalid')

    return render(request, 'set_buget.html', d)
    

