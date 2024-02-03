from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, AddTransactionForm, AddBudgetForm, AddIncomeForm
from .models import Transaction, Budget, Income, OrdinaryUser
import datetime
from abc import ABC, abstractclassmethod

class UserController():
	@abstractclassmethod
	def register_user(request):
		pass

	def logout_user(request):
		pass
	
class StandartUserController(UserController):
	def register_user(request):
		if request.method == 'POST': 
			form = SignUpForm(request.POST)
			if form.is_valid():
				form.save()
				username = form.cleaned_data['username']
				password = form.cleaned_data['password1']
				user = authenticate(username=username, password=password)
				login(request, user)
				messages.success(request, "Вы зарегистрированы.")
				return redirect('home')
		else:
			form = SignUpForm()
			return render(request, 'register.html', {'form':form})
		return render(request, 'register.html', {'form':form})
	
	def logout_user(request):
		logout(request)
		messages.success(request, "Вы вышли из учетной записи.")
		return redirect('home')
	
class FinanceStateController():
	@abstractclassmethod
	def budgets():
		pass

	@abstractclassmethod
	def incomes():
		pass

	@abstractclassmethod
	def transactions():
		pass

class StandartFinanceStateController(FinanceStateController):

	def home(request):
		current_user = OrdinaryUser.objects.all()[0]
		transactions = Transaction.objects.all().order_by("-time")[:6]
		last_spend =  Transaction.objects.filter(sum__lt=0).order_by("-time")[0]
		last_income =  Transaction.objects.filter(sum__gt=0).order_by("-time")[0]
		spend_sum = last_spend.sum
		spend_time = last_spend.time
		income_sum = last_income.sum
		income_time = last_income.time
		if request.method == 'POST':
			username = request.POST['username']
			password=request.POST['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, 'Вы не зарегистрированы.')
			return redirect('home')
		else:
			return render(request, 'home.html', {'transactions':transactions,
										'balance':current_user.balance,
										'spend_sum':spend_sum,
										'spend_time':spend_time, 
										'income_sum':income_sum,
										'income_time':income_time})


		
	def budgets(request):
		transactions = Transaction.objects.all()
		budgets = Budget.objects.all()
		properties = dict()
		for i in range(len(budgets)):
			properties[budgets[i]] = [budgets[i].percentage(),budgets[i].total_spent(),budgets[i].average_daily(),budgets[i].saved()]
		if request.user.is_authenticated:
			return render(request, 'budgets.html', {'budgets':budgets, 'transactions': transactions})
		
	def add_transaction(request):
		form = AddTransactionForm(request.POST or None)
		if request.user.is_authenticated:
			if request.method == "POST":
				if form.is_valid():
					add_transaction = form.save()
					sum = add_transaction.sum
					user = OrdinaryUser.objects.all()[0]
					user.balance = user.balance+sum
					user.save()
					#user.update_balance(sum)
					messages.success(request, "Запись добавлена.")
					return redirect('home')
			return render(request, 'add_transaction.html', {'form':form})
		else:
			messages.success(request, "Вы должны зайти в учетную запись.")
			return redirect('home')
		
	def one_transaction(request, pk):
		if request.user.is_authenticated:
			one_transaction = Transaction.objects.get(id=pk)
			return render(request, 'transaction.html', {'one_transaction':one_transaction})
		else:
			messages.success(request, 'Вы не зарегистрированы.')
			return redirect('home')
		
	def delete_transaction(request, pk):
		if request.user.is_authenticated: 
			delete_it = Transaction.objects.get(id=pk)
			delete_it.delete()
			messages.success(request, "Запись удалена.")
			return redirect('home')  
		else:
			messages.success(request, 'Вы не зарегистрированы.')
			return redirect('home') 
		
	def add_budget(request):
		form = AddBudgetForm(request.POST or None)
		if request.user.is_authenticated:
			if request.method == "POST":
				if form.is_valid():
					add_budget = form.save()
					messages.success(request, "Запись добавлена.")
					return redirect('budgets')
			return render(request, 'add_budget.html', {'form':form})
		else:
			messages.success(request, "Вы должны зайти в учетную запись.")
			return redirect('home')


	def incomes(request):
		transactions = Transaction.objects.all()
		incomes = Income.objects.all()
		if request.user.is_authenticated:
			return render(request, 'incomes.html', {'incomes':incomes, 'transactions': transactions})
		else:
			messages.success(request, 'Вы не зарегестрированы')
			return redirect('home')

	def add_income(request):
		form = AddIncomeForm(request.POST or None)
		if request.user.is_authenticated:
			if request.method == "POST":
				if form.is_valid():
					add_income = form.save()
					messages.success(request, "Запись добавлена.")
					return redirect('incomes')
			return render(request, 'add_income.html', {'form':form})
		else:
			messages.success(request, "Вы должны зайти в учетную запись.")
			return redirect('incomes')
		
	def one_income(request, pk):
		if request.user.is_authenticated:
			one_income = Income.objects.get(id=pk)
			return render(request, 'income.html', {'one_income':one_income})
		else:
			messages.success(request, 'Вы не зарегистрированы.')
			return redirect('incomes')
		
	def delete_income(request, pk):
		if request.user.is_authenticated: 
			delete_it = Income.objects.get(id=pk)
			delete_it.delete()
			messages.success(request, "Запись удалена.")
			return redirect('incomes')  
		else:
			messages.success(request, 'Вы не зарегистрированы.')
			return redirect('incomes') 