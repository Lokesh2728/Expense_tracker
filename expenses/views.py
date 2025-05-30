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
from .signals import *
from itertools import chain
from django.utils import timezone



# Create your views here.
def home(request):
    user = request.user  
    balance = Balance.objects.filter(user_id=request.user).last()
    montly_budget=Buget.objects.filter(username=user).first()
    Sett=Buget.objects.filter(username=user).values_list('monthly_set', flat=True).first()
    monthly_expense=Expense.objects.filter(username=user).aggregate(Sum('amount'))['amount__sum'] or 0 
    recent_transactions = Transaction.objects.filter(user_id=user).order_by('-id')[:3]
    percentage_spent = (monthly_expense / Sett) * 100 if Sett else 0


    d = {
        'recent_transactions': recent_transactions,
        'balance':balance,
        'monthly_expense':monthly_expense,
        'montly_budget':montly_budget,
        'percentage_spent':percentage_spent
        

    }
    return render(request, 'home.html', d)



@login_required
def dashboard(request):
    user = request.user
    monthly_expense = Expense.objects.filter(username=user).aggregate(Sum('amount'))['amount__sum'] or 0 
    monthly_budget_obj = Buget.objects.filter(username=user).first()
    monthly_budget = monthly_budget_obj.monthly_set if monthly_budget_obj else 0
    percentage = (float(monthly_expense) / float(monthly_budget)) * 100 if monthly_budget else 0

    # Generate charts
    daily_Expense(user)
    pie_chart(user)
    monthly_expense_trend(user)
    current_month_daily_trend(user)

    context = {
        'has_expense': monthly_expense > 0,
        'monthly_expense': monthly_expense,
        'monthly_budget': monthly_budget,  
        'percentage': round(percentage, 2),
        'insight': f"You’ve spent {round(percentage, 2)}% of your budget",
        'bar_chart': 'expenses/static/charts/bar_chart.png',
        'pie_chart': 'expenses/static/charts/pie_chart.png',
        'line_chart': 'expenses/static/charts/monthly_expense_trend.png',
        'current_month_trend': 'expenses/static/charts/current_month_trend.png',  # fixed path
    }

    return render(request, 'dashboard.html', context)





class AddExpense(LoginRequiredMixin,CreateView):
    model=Expense
    form_class = ExpenseForm
    template_name='AddExpense.html'
    success_url=reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs['user']=self.request.user
        return kwargs
    

    def form_valid(self, form):
        user = self.request.user
        form.instance.username = user
        new_amount = form.cleaned_data['amount']

        # Get latest total_balance
        latest_balance = Balance.objects.filter(user_id=user).order_by('-created_at', '-time').first()
        previous_total = latest_balance.total_balance if latest_balance else 0


        if new_amount > previous_total:
            form.add_error('amount', 'Insufficient balance to complete this transaction.')
            return self.form_invalid(form)  # Return error and re-render form

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

        category = Expense.objects.filter(username_id=user).order_by('-date').values_list('category', flat=True).first()
        transaction.send(
            sender=AddExpense,user=user,
            request=self.request,
            transaction_amount=new_amount,
            category=category
            
            )

        return super().form_valid(form)



class ExpenseList(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'ExpenseList.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user_id=self.request.user).order_by('-id')


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
        updated_total = previous_total + new_amount
        form.instance.total_balance = updated_total


        creditedAmount.send(
            sender=Balanceview,
            user=self.request.user,
            request=self.request,
            credited_amount=form.cleaned_data['balance']
        )



        

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
            budget_obj.monthly_set=budget
            budget_obj.last_alert_level = 0  
            budget_obj.save()

            return HttpResponse('created')
        else:
            return HttpResponse('invalid')

    return render(request, 'set_buget.html', d)
    

