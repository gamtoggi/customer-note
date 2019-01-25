from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    # /customers
    path('', views.customer_list, name='list'),

    # /customers/ajax
    path('ajax', views.customer_list_ajax, name='list_ajax'),

    # /customers/1
    path('<int:pk>', views.customer_detail, name='detail'),

    # /customers/1/ajax
    path('<int:pk>/ajax', views.customer_detail_ajax, name='detail_ajax'),

    # /customers/1/contacts
    path('<int:pk>/contacts', views.customer_detail_contacts, name='detail_contacts'),

    # /customers/1/contacts/ajax
    path('<int:pk>/contacts/ajax', views.customer_detail_contacts_ajax, name='detail_contacts_ajax'),

    # /customers/1/purchases
    path('<int:pk>/purchases', views.customer_detail_purchases, name='detail_purchases'),

    # /customers/1/purchases/ajax
    path('<int:pk>/purchases/ajax', views.customer_detail_purchases_ajax, name='detail_purchases_ajax'),

    # /customers/create/ajax
    path('create/ajax', views.customer_create_ajax, name='create_ajax'),

    # /customers/1/update/ajax
    path('<int:pk>/update/ajax', views.customer_update_ajax, name='update_ajax'),
]
