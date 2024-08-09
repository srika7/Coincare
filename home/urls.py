from django.urls import path
from .views import home, delete_expense, history_view

urlpatterns = [
    path('', home, name='home'),
    path('delete/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('history/', history_view, name='history_view'),
]
