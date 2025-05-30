from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver,Signal
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import *
from django.db.models import Sum



creditedAmount = Signal()


@receiver(creditedAmount)
def Amount_credited(sender, user, request, credited_amount, **kwargs):
    email = user.email  
    print(f"✅ Amount has been credited to: {email} account")

    send_mail(
        subject='Amount Credited',
        message=f'Your account xxxxx has been credited with ₹{credited_amount}.',
        from_email='lokeshpatel2714@gmail.com',
        recipient_list=[email],
        fail_silently=True,
    )



transaction=Signal()
@receiver(transaction)
def Transaction_made(sender, user, request, transaction_amount,category, **kwargs):
    email = user.email
    print(f"✅ Amount has been Debited from: {email}'s account")

    send_mail(
                subject='✅ Transaction Alert: Amount Debited',
                message=f'''Dear {email},
We are pleased to inform you that a transaction has been successfully made to your account.
🧾 Transaction Details:
• Amount       : ₹{transaction_amount}
• Category     : {category}
• Date & Time  : {now().strftime('%d %B %Y at %I:%M %p')}

Thank you for banking with us. If you have any questions, feel free to contact support.

Warm regards,  
💼 Your Finance Team
                    ''',
                        from_email='lokeshpatel2714@gmail.com',
                        recipient_list=[email],
                        fail_silently=True,
            )


@receiver(post_save, sender=Expense)
def create_transaction_from_expense(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            user=instance.username,  
            transaction_type='Debit',
            amount=instance.amount,
            category=instance.category if hasattr(instance, 'category') else ''
        )

@receiver(post_save, sender=Balance)
def create_transaction_from_balance(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            user=instance.user_id,  
            transaction_type=instance.Transactin_type, 
            amount=instance.balance,
            category=''  
        )


@receiver(post_save, sender=Expense)
def budget_alert_email(sender, instance, created, **kwargs):
    if not created:
        return

    user=instance.username
    total_expense = Expense.objects.filter(username=user).aggregate(Sum('amount'))['amount__sum'] or 0 
    budget_obj = Buget.objects.filter(username=user).first()

    if not budget_obj or budget_obj.budget == 0:
        return

    used_percentage = (total_expense /(total_expense + budget_obj.budget)) * 100  # % used from original budget



    subject = None
    message = None
    if  used_percentage >= 50:
        subject = "🟡 50%  of your budget used!"
        message = f"Hi ,\n\nYou've used 50% of your monthly budget. Keep an eye on your spending!"
        budget_obj.last_alert_level = 50



    elif  used_percentage >= 90:
        subject = "🔴 90% of your budget used!"
        message = f"Hi ,\n\nYou've used 90% of your monthly budget. You might want to slow down spending."
        budget_obj.last_alert_level = 90
        budget_obj.save()

    if subject:
        send_mail(
            subject,
            message,
            from_email='lokeshpatel2714@gmail.com',
            recipient_list=[user.email],
            fail_silently=True,
        )