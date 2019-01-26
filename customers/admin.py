from django.contrib import admin

from .models import Customer, Contact, Purchase

admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Purchase)
