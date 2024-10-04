from django.contrib import admin
from . models import Account
# Register your models here.

@admin.register(Account)
class AccountModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'is_active']
