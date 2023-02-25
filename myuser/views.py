from django.shortcuts import render ,redirect
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
import json


@login_required(login_url='/login')
def general(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
 

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':

        return render(request, 'general.html', {'currencies': currency_data,
                                                          'user_preferences': user_preferences})
    else:

        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')

        return render(request, 'general.html', {'currencies': currency_data, 'user_preferences': user_preferences})

@login_required(login_url='/login')    
def expense(request):    

    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    a = str(currency)
    a = a[:3]
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': a
    }

    return render(request,'expense.html',context)


@login_required(login_url='/login')    
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    
    if request.method == 'POST':
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        amount = request.POST['amount']

        if date :

            Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        else : 
            Expense.objects.create(owner=request.user, amount=amount,
                               category=category, description=description)
        
        messages.success(request, 'Expense saved successfully')                       

    return render(request,'add_expense.html',context)

@login_required(login_url='/login')    
def expense_edit(request,id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    
    if request.method == 'GET':
        return render(request, 'edit_expense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        



        expense.owner = request.user
        expense.amount = amount
        expense. date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('user_expense')

@login_required(login_url='/login')    
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('user_expense')

@login_required(login_url='/login')    
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/login')
def income(request):

    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    a = str(currency)
    a = a[:3]
    
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': a
    }

    return render (request,'income.html', context)


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        if date :
            UserIncome.objects.create(owner=request.user, amount=amount, date=date,
                                  source=source, description=description)
        
        
        else :
            UserIncome.objects.create(owner=request.user, amount=amount, 
                                  source=source, description=description)
        
        messages.success(request, 'Record saved successfully')

        return render(request, 'add_income.html', context)


@login_required(login_url='/login')
def edit_income(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        income.amount = amount
        income. date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, 'Record updated  successfully')

        return redirect('user_income')

@login_required(login_url='/login')
def delete_income(request,id):

    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request,'Income Deleted')

    return redirect('user_income')
