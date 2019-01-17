from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    # GET /customers
    path('', views.CustomerListView.as_view(), name='index'),

    # /customers/create
    path('create', views.CustomerCreateView.as_view(), name='create'),

]
