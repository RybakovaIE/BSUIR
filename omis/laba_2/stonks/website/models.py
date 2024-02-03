from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, date
    
class OrdinaryUser(User):
    balance = models.FloatField('Баланс')

    def update_balance(self, sum):
        self.balance = self.balance + sum

class Transaction(models.Model):
    sum = models.FloatField('Сумма транзакции')
    time = models.DateTimeField('Дата и время')
    category = models.CharField('Категория бюджета', max_length = 35)
    user = User('Пользователь')

    def ago(self):
        return datetime.now() - self.time

class Budget(models.Model):
    name = models.CharField('Название', max_length = 35)
    limit = models.FloatField('Лимит средств')
    user = User('Пользователь')

    def average_daily(self):
        transactions = Transaction.objects.filter(category=self.name)
        last = Transaction.objects.order_by("-time")[0].time
        first = Transaction.objects.order_by("time")[0].time
        days = last-first
        days = int(str(days).split(',')[0].split(' ')[0])
        total_spent = self.total_spent()
        return round(total_spent/days, 2)

    def saved(self):
        if self.percentage() > 100: return ':('
        daily = self.average_daily()
        return round(self.limit-(30*daily), 2)
    
    def total_spent(self):
        transactions = Transaction.objects.filter(category=self.name)
        return sum(abs(transaction.sum) for transaction in transactions)
    
    def percentage(self):
        return int(self.total_spent()/self.limit*100)

class Income(models.Model):
    name = models.CharField('Название', max_length = 35)
    sum = models.FloatField('Сумма')
    time = models.DateField('Дата начисления')
    user = User('Пользователь')

    def before(self):
        ya = ['2', '3', '4']
        number =  str(self.time - date.today()).split(',')[0].split(' ')[0]
        if number[-1] == '1': days = ' день'
        elif number[-1] in ya: days = ' дня'
        else: days = ' дней'
        return number + days