from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
# Create your models here.
class Expense(models.Model):


    CATEGORY_CHOICES = (
    ('Food', 'Food'),
    ('Transport', 'Transport'),
    ('Shopping', 'Shopping'),
    ('Utilities', 'Utilities'),
    ('Health', 'Health'),
    ('Other', 'Other'),
)
    username = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)
    category = models.CharField( max_length=10 ,choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
    

class Balance(models.Model):
    user_id=models.ForeignKey("accounts.UserProfile",on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    Transactin_type=models.CharField(max_length=10,null=True)
    balance=models.DecimalField( max_digits=10, decimal_places=2,default=0)
    total_balance=models.DecimalField( max_digits=10, decimal_places=2,default=0)
    time=models.TimeField(auto_now=True)

    def clean(self):
        if self.Transactin_type == 'Debit' and self.total_balance < 0:
            raise ValidationError("Insufficient funds! Cannot perform debit that results in negative balance.")
        
    def __str__(self):
        return f"{self.user_id} - {self.Transactin_type} - ₹{self.balance}"


class Buget(models.Model):
    monthly_set=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    budget=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    username=models.ForeignKey("accounts.UserProfile",on_delete=models.CASCADE)
    last_alert_level = models.IntegerField(default=0)
    last_reset = models.DateField(default=timezone.now)

   
    def __str__(self):
        return str(self.budget)
    


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Debited', 'Debited'),
        ('Credited', 'Credited'),
    )
    
    user = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True, null=True)  # optional for expenses
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.user.username}"