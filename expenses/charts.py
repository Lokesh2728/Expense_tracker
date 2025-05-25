import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .models import Expense
from accounts.models import UserProfile
from datetime import datetime, date
import os
from django.conf import settings
import calendar
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay

# ========== DAILY BAR CHART ==========
def daily_Expense(user):
    user_profile = UserProfile.objects.get(email=user)
    expenses = Expense.objects.filter(username=user_profile, date__month=datetime.now().month)

    daily_total = {}
    for exp in expenses:
        day = exp.date.day
        daily_total[day] = daily_total.get(day, 0) + float(exp.amount)

    days = sorted(daily_total.keys())
    amounts = [daily_total[day] for day in days]

    plt.figure(figsize=(5,5))
    bars = plt.bar(days, amounts, color='#4A90E2', edgecolor='black')
    plt.title('Daily Expenses This Month', fontsize=14, weight='bold')
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Amount', fontsize=12)
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(days, rotation=45)
    plt.tight_layout()

    chart_path = os.path.join(settings.BASE_DIR, 'expenses/static/charts/bar_chart.png')
    plt.savefig(chart_path)
    plt.close()


# ========== PIE CHART ==========
def pie_chart(user):
    user_profile = UserProfile.objects.get(email=user)
    expenses = Expense.objects.filter(username=user_profile)

    category_totals = {}
    for exp in expenses:
        category = exp.category
        amount = float(exp.amount)
        category_totals[category] = category_totals.get(category, 0) + amount

    labels = list(category_totals.keys())
    values = [category_totals[label] for label in labels]
    colors = ['orange', 'red', 'blue', 'green', 'pink']

    explode = [0.05] * len(labels)

    plt.figure(figsize=(5, 5))
    wedges, texts, autotexts = plt.pie(
        values,
        labels=None,
        autopct='%1.0f%%',
        startangle=140,
        colors=colors,
        explode=explode,
        shadow=True,
        textprops={'fontsize': 10},
        center=(0, 0)
    )

    plt.setp(autotexts, size=10, weight='bold')
    plt.title('Expenses by Category', fontsize=14, weight='bold')
    plt.legend(wedges, labels, title="Categories", loc="lower center", bbox_to_anchor=(1, 0, 0.5, 1),ncol=2)

    plt.axis('equal')
    plt.tight_layout()

    chart_path = os.path.join(settings.BASE_DIR, 'expenses/static/charts/pie_chart.png')
    plt.savefig(chart_path)
    plt.close()


# ========== MONTHLY EXPENSE TREND ==========
def monthly_expense_trend(user):
    expenses = (
        Expense.objects
        .filter(username_id=user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    if not expenses:
        return None

    months = [calendar.month_name[e['month'].month] for e in expenses]
    totals = [float(e['total']) for e in expenses]

    plt.figure(figsize=(6, 4))
    plt.plot(months, totals, marker='o', linestyle='-', color='#4A90E2', linewidth=2)
    plt.title('Monthly Expense Trend', fontsize=14, weight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Expense', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()

    chart_path = os.path.join(settings.BASE_DIR, 'expenses/static/charts/monthly_expense_trend.png')
    plt.savefig(chart_path)
    plt.close()


# ========== CURRENT MONTH DAILY TREND ==========
def current_month_daily_trend(user):
    today = date.today()
    expenses = (
        Expense.objects
        .filter(username_id=user, date__year=today.year, date__month=today.month)
        .annotate(day=TruncDay('date'))
        .values('day')
        .annotate(total=Sum('amount'))
        .order_by('day')
    )

    if not expenses:
        return None

    days = [e['day'].day for e in expenses]
    totals = [float(e['total']) for e in expenses]

    plt.figure(figsize=(6, 4))
    plt.plot(days, totals, marker='o', linestyle='-', color='green', linewidth=2)
    plt.title('Daily Spending Trend - Current Month', fontsize=14, weight='bold')
    plt.xlabel('Day of Month', fontsize=12)
    plt.ylabel('Expense Amount', fontsize=12)
    # plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    chart_path = os.path.join(settings.BASE_DIR, 'expenses/static/charts/current_month_trend.png')
    plt.savefig(chart_path)
    plt.close()
