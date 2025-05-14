from django.db import models
from django.conf import settings
# Create your models here.
class Expense(models.Model):
    username = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
