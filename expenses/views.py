from django.shortcuts import render,redirect
from django.views.generic import  CreateView,ListView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from expenses.models import *
from expenses.forms import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse



# Create your views here.
def home(request):
    user = request.user  
    monthly_expense=Expense.objects.filter(username=user).aggregate(Sum('amount'))['amount__sum'] or 0 
    recent_transactions = Expense.objects.filter(username=user).order_by('-id')[:3]
    balance = Balance.objects.filter(user_id=request.user).first()
    montly_budget=Buget.objects.filter(username=user).first()
    d = {
        'recent_transactions': recent_transactions,
        'balance':balance,
        'monthly_expense':monthly_expense,
        'montly_budget':montly_budget,
    }
    return render(request, 'home.html', d)



class AddExpense(LoginRequiredMixin,CreateView):
    model=Expense
    form_class = ExpenseForm
    template_name='AddExpense.html'
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        form.instance.username = self.request.user
        new_amount = form.cleaned_data['amount']

        # deduting the balance from my account 
        balance_obj=Balance.objects.get(user_id=self.request.user)
        balance_obj.balance -= new_amount
        balance_obj.save()

        #deducting the balace from my monthly limit
        monthly_limit=Buget.objects.get(username=self.request.user)
        monthly_limit.budget -= new_amount
        monthly_limit.save()
        return super().form_valid(form)


class ExpenseList(LoginRequiredMixin,ListView):
    model=Expense
    template_name='ExpenseList.html'
    context_object_name='expenseobject'


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
        new_amount = form.cleaned_data['balance']
        balance_obj=Balance.objects.get_or_create(user_id=user)[0]
        balance_obj.balance += new_amount
        balance_obj.save()
        return redirect(self.success_url)

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
    
