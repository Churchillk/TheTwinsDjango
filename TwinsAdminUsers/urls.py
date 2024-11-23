from django.urls import path
from .views import (
    TwinsDrinksListView,
    DashView, custom_admin_login, DeleteUser,
    TwinsSoldDrinksListView, TwinsAddedDrinksListView,
    TwinsExpensesListView, AddExpenses, UpdateUser,
    TwinsOrderedDrinksListView, Debts, AllUsers,
    AddDrink, UpdateDrink, DeleteDrink, add_user
)

urlpatterns = [
    path('', custom_admin_login, name='admin_login'),
    path('admin-dash/', DashView.as_view(), name='admin_dash'),
    path('twins-drinks/', TwinsDrinksListView.as_view(), name='twins_drinks_list'),
    path('add-drinks-twins/', AddDrink.as_view(), name='add_drink_twins'),
    path('twins-sold-drinks/', TwinsSoldDrinksListView.as_view(), name='twins_sold_drinks'),
    path('twins-added-drinks/', TwinsAddedDrinksListView.as_view(), name='twins_added_drinks'),
    path('drinks/update/<int:pk>/', UpdateDrink.as_view(), name='update_drink'),
    path('drinks/delete/<int:pk>/', DeleteDrink.as_view(), name='delete_drink'),
    path('twins-ordered-drinks/', TwinsOrderedDrinksListView.as_view(), name='twins_ordered_drinks'),
    path('add-expense-twins/', AddExpenses.as_view(), name='add_expense_twins'),
    path('twins-expenses/', TwinsExpensesListView.as_view(), name='twins-expenses'),
    path('all-users/', AllUsers.as_view(), name='users'),
    path('add-employee/', add_user, name='add_employee'),
    path("Update-user/<int:pk>/", UpdateUser.as_view(), name = 'update_user'),
    path("all-users/delete-user/<int:pk>/", DeleteUser.as_view(), name='delete_user'),
    path("twins-debtors/", Debts.as_view(), name='twins_debtors'),
]