from django.contrib import admin

from .models import Assets , DepositHistory , News
# Register your models here.

admin.site.register(Assets)
admin.site.register(DepositHistory)
admin.site.register(News)