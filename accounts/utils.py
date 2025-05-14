from accounts.models import UserProfile


def custom_authenticate(email, password):
    try:
        user = UserProfile.objects.get(email=email)
        if user.check_password(password):  
            return user
        else:
            return None
    except UserProfile.DoesNotExist:
        return None
