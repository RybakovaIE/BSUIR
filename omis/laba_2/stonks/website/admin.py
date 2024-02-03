from django.contrib import admin
from .models import Transaction, Budget, Income, OrdinaryUser

admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Income)
admin.site.register(OrdinaryUser)