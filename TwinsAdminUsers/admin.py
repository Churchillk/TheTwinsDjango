from django.contrib import admin
from .models import StoreDrinks, StoreSoldDrinks, StoreExpenses, StoreOrderedDrinks

@admin.register(StoreDrinks)
class StoreDrinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'wholesale', 'cost', 'opening_stock', 'added_stock', 'sold_stock', 'closing_stock')
    search_fields = ('name',)
    list_filter = ('closing_stock',)
    readonly_fields = ('closing_stock',)

@admin.register(StoreSoldDrinks)
class StoreSoldDrinksAdmin(admin.ModelAdmin):
    list_display = ('drink', 'quantity', 'status', 'total', 'date', 'payment_mode', 'customer', 'customer_contact')
    search_fields = ('drink__name', 'customer')
    list_filter = ('status', 'payment_mode', 'date')
    readonly_fields = ('total',)

@admin.register(StoreExpenses)
class StoreExpensesAdmin(admin.ModelAdmin):
    list_display = ('employee', 'expense', 'price', 'date')
    search_fields = ('employee__username', 'expense')
    list_filter = ('date',)

@admin.register(StoreOrderedDrinks)
class StoreOrderedDrinksAdmin(admin.ModelAdmin):
    list_display = ('drink', 'order_number', 'product_cost', 'payment_mode', 'start_date', 'order_status')
    search_fields = ('order_number', 'drink__name')
    list_filter = ('order_status', 'payment_mode', 'start_date')
    readonly_fields = ('order_number',)

# Ensure to register the admin classes with the models
