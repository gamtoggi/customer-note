from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    # /customers/
    path('', views.CustomerListView.as_view(), name='index'),
]
