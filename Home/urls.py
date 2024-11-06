from django.urls import path
from Home import views as HomeViews

urlpatterns = [
    path('', HomeViews.HomeView.as_view(), name="home"),
    path('drinks/', HomeViews.DrinksView.as_view(), name="drinks"),
    path('drinks/<int:pk>/', HomeViews.SellDrink.as_view(), name="selldrink"),
    path('sold_drinks/', HomeViews.SoldDrinksView.as_view(), name="sold_drinks"),
    path('orderd_drinks/', HomeViews.OrderedDrinksView.as_view(), name="orderd_drinks"),
    path('added_drinks/', HomeViews.AddedDrinksView.as_view(), name="added_drinks"),
    path('expenses/', HomeViews.ExpensesView.as_view(), name="expenses"),
    path('add_expense/', HomeViews.AddExpenses.as_view(), name="add_expense"),
    path('contacts/', HomeViews.ContactsView.as_view(), name='contacts'),
    path('debts/', HomeViews.Debts.as_view(), name="debts"),
    path('daily-report/', HomeViews.DailyReportView.as_view(), name='daily_report'),
]
