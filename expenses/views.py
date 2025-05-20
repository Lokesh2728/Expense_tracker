from django.shortcuts import render
from django.views.generic import  CreateView,ListView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from expenses.models import *
from expenses.forms import *
from django.urls import reverse_lazy

# Create your views here.


class AddExpense(LoginRequiredMixin,CreateView):
    model=Expense
    form_class = ExpenseForm
    template_name='AddExpense.html'
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        form.instance.username = self.request.user
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

