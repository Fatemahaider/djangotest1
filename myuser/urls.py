from django.urls import path
from . import views
from .views import *
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [

    path('general/',general,name='user_general'),
    path('expense/',expense,name='user_expense'),
    path('expense/add',add_expense,name='add_expense'),
    path('expense/edit/<int:id>',expense_edit,name='expense_edit'),
    path('expense/delete/<int:id>',delete_expense,name='delete_expense'),
    path('search_expenses',csrf_exempt(search_expenses),name='search_expenses'),
    path('income/',income,name='user_income'),
    path('income/add',add_income,name='add_income'),
    path('income/edit/<int:id>',edit_income,name='edit_income'),
    path('income/delete/<int:id>',delete_income,name='delete_income'),
    path('search_income',csrf_exempt(search_income),name='search_income'),

] 




