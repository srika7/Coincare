from django.shortcuts import redirect, render, get_object_or_404
from .models import Profile, Expense

def home(request):
    profile = Profile.objects.filter(user=request.user).first()
    expenses = Expense.objects.filter(user=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        expense_type = request.POST.get('type')

        if not name or not amount or not expense_type:
            return render(request, 'home.html', {
                'profile': profile,
                'expenses': expenses,
                'error': 'All fields are required.'
            })
        
        try:
            amount = float(amount)
        except ValueError:
            return render(request, 'home.html', {
                'profile': profile,
                'expenses': expenses,
                'error': 'Invalid amount.'
            })

        expense = Expense(name=name, amount=amount, expense_type=expense_type, user=request.user)
        expense.save()

        if expense_type == 'Positive':
            profile.balance += amount
            profile.income += amount
        else:
            profile.expense += amount
            profile.balance -= amount
        
        profile.save()
        return redirect('/')

    context = {
        'profile': profile,
        'expenses': expenses
    }
    return render(request, 'home.html', context)

from django.shortcuts import redirect, render, get_object_or_404
from .models import Profile, Expense

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    profile = Profile.objects.get(user=request.user)

    if expense.expense_type == 'Positive':
        profile.balance -= expense.amount
        profile.income -= expense.amount
    else:
        profile.expense -= expense.amount
        profile.balance += expense.amount
    
    profile.save()
    expense.delete()

    return redirect('/')


def history_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-amount')
    return render(request, 'history.html', {'expenses': expenses})
