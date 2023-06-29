from django.contrib import admin
from .models import UserAccount, UserTransaction
# Register your models here.

admin.site.register(UserAccount)
admin.site.register(UserTransaction)