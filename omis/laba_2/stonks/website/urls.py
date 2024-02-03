from . import views
from django.urls import path

urlpatterns = [
    path('', views.StandartFinanceStateController.home, name='home'),
    path('logout/', views.StandartUserController.logout_user, name='logout'),
    path('register/', views.StandartUserController.register_user, name='register'),
    path('add_transaction/', views.StandartFinanceStateController.add_transaction, name='add_transaction'),
    path('transaction/<int:pk>', views.StandartFinanceStateController.one_transaction, name='transaction'),
    path('delete_transaction/<int:pk>', views.StandartFinanceStateController.delete_transaction, name='delete_transaction'),
    path('add_budget/', views.StandartFinanceStateController.add_budget, name='add_budget'),
    path('add_income/', views.StandartFinanceStateController.add_income, name='add_income'),
    path('income/<int:pk>', views.StandartFinanceStateController.one_income, name='income'),
    path('delete_income/<int:pk>', views.StandartFinanceStateController.delete_income, name='delete_income'),
    path('incomes/', views.StandartFinanceStateController.incomes, name = 'incomes'),
    path('budgets/', views.StandartFinanceStateController.budgets, name = 'budgets'),
]
