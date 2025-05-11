from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


class UserProfileManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,password='None'):
        if not email:
            raise ValueError('email is not provided')
        nemail=self.normalize_email(email)
        UO=self.model(email=email,first_name=first_name,last_name=last_name)
        UO.set_password(password)
        UO.save()
        return UO
    def create_superuser(self,email,first_name,last_name,password):
        UO=self.create_user(email,first_name,last_name,password)
        UO.is_staff=True
        UO.is_superuser=True
        UO.save()


class UserProfile(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(primary_key=True)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField( max_length=50)
    is_active=models.BooleanField(default= True)
    is_superuser=models.BooleanField(default= False)
    is_staff=models.BooleanField(default= False)
    objects=UserProfileManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name']
