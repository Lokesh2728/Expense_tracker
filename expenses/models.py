from django.db import models
from django.urls import reverse
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
    balance=models.DecimalField( max_digits=10, decimal_places=2,default=0)
    user_id=models.ForeignKey("accounts.UserProfile",on_delete=models.CASCADE)

    