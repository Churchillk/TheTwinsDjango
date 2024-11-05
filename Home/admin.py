from django.contrib import admin
from . import models as HomeModels

admin.site.site_header = 'Twins Dev'
admin.site.index_title = 'DevAdmin'

@admin.register(HomeModels.Dashboard)
class AdminDash(admin.ModelAdmin):
    list_display = [field.name for field in HomeModels.Dashboard._meta.get_fields()]

@admin.register(HomeModels.Drinks)
class AdminDrinks(admin.ModelAdmin):
    list_display = ('name', 'cost', 'opening_stock', 'added_stock', 'sold_stock', 'closing_stock')
    
@admin.register(HomeModels.SoldDrinks)
class  AdminSoldDrinks(admin.ModelAdmin):
    list_display = ('drink', 'customer', 'quantity', 'status', 'total' ,'date')
    
@admin.register(HomeModels.OrderedDrinks)
class OrderedDrinksAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'drink', 'product_cost', 'payment_mode', 'start_date', 'order_status')
    search_fields = ('order_number', 'drink__name', 'payment_mode')
    list_filter = ('order_status', 'payment_mode')
    ordering = ('-start_date',)
    
@admin.register(HomeModels.Contact)
class RegContact(admin.ModelAdmin):
    list_display = ['name', 'contact', 'role', 'location']
    
@admin.register(HomeModels.MessageUser)
class RegMessage(admin.ModelAdmin):
    list_display = ['name', 'message']
    
@admin.register(HomeModels.Expenses)
class AdminExpens(admin.ModelAdmin):
    list_display = [field.name for field in HomeModels.Expenses._meta.get_fields()]