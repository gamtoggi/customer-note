from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    # /customers
    path('', views.customer_index, name='index'),

    # /customers/list
    path('list', views.customer_list, name='list'),

    # /customers/1
    path('<int:pk>', views.customer_detail, name='detail'),

    # /customers/create
    path('create', views.customer_create, name='create'),

    # /customers/1/update
    path('<int:pk>/update', views.customer_update, name='update'),
]
