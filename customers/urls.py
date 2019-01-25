from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    # /customers
    path('', views.customer_list, name='list'),

    # /customers/ajax
    path('ajax', views.customer_ajax_list, name='ajax_list'),

    # /customers/1
    path('<int:pk>', views.customer_detail, name='detail'),

    # /customers/ajax/1
    path('ajax/<int:pk>', views.customer_ajax_detail, name='ajax_detail'),

    # /customers/ajax/create
    path('ajax/create', views.customer_ajax_create, name='ajax_create'),

    # /customers/ajax/1/update
    path('ajax/<int:pk>/update', views.customer_ajax_update, name='ajax_update'),
]
