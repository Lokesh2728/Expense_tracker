#importing  necessary libraries 
import matplotlib.pyplot as plt
from .models import *
from accounts.models import UserProfile
from datetime import datetime
import os
from django.conf import settings



#bar chart for daily expenses

def daily_Expense(user):
    # Filter expenses for the current month
    user_profile = UserProfile.objects.get(email=user)

    expenses = Expense.objects.filter(username=user_profile , date__month=datetime.now().month)
    daily_total={}

    for exp in expenses:
        print(exp.date, type(exp.date))
        day=exp.date.day
        daily_total[day]=daily_total.get(day,0)+float(exp.amount)

    days=sorted(daily_total.keys())
    amounts=[daily_total[day] for day in days]

    #Bar chart  
    plt.figure(figsize=(5,4))
    plt.bar(days, amounts, color='skyblue')
    plt.title('Daily Expenses This Month')
    plt.xlabel('Day')
    plt.ylabel('Amount')
    plt.tight_layout()

    chart_path = os.path.join(settings.BASE_DIR, 'expenses/static/charts/bar_chart.png')
    plt.savefig(chart_path)
    plt.close()

