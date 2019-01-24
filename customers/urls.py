from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    # /customers
    path('', views.customer_list, name='index'),

    # /customers/create
    path('create', views.customer_create, name='create'),
]
