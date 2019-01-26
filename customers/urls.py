from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    # /customers
    path('', views.customer_list, name='list'),

    # /customers/ajax
    path('ajax', views.customer_list_ajax, name='list_ajax'),

    # /customers/create/ajax
    path('create/ajax', views.customer_create_ajax, name='create_ajax'),

    # /customers/1/update/ajax
    path('<int:pk>/update/ajax', views.customer_update_ajax, name='update_ajax'),

    # /customers/1/info
    path('<int:pk>/info', views.customer_info, name='info'),

    # /customers/1/info/ajax
    path('<int:pk>/info/ajax', views.customer_info_ajax, name='info_ajax'),

    # /customers/1/contacts
    path('<int:pk>/contacts', views.customer_contacts, name='contacts'),

    # /customers/1/contacts/ajax
    path('<int:pk>/contacts/ajax', views.customer_contacts_ajax, name='contacts_ajax'),

    # /customers/1/contacts/create/ajax
    path('<int:pk>/contacts/create/ajax', views.customer_contacts_create_ajax, name='contacts_create_ajax'),

    # /customers/1/contacts/1/update/ajax
    path('<int:pk>/contacts/<int:contact_pk>/update/ajax', views.customer_contacts_update_ajax, name='contacts_update_ajax'),

    # /customers/1/purchases
    path('<int:pk>/purchases', views.customer_purchases, name='purchases'),

    # /customers/1/purchases/ajax
    path('<int:pk>/purchases/ajax', views.customer_purchases_ajax, name='purchases_ajax'),

    # /customers/1/purchases/create/ajax
    path('<int:pk>/purchases/create/ajax', views.customer_purchases_create_ajax, name='purchases_create_ajax'),

    # /customers/1/purchases/1/update/ajax
    path('<int:pk>/purchases/<int:purchase_pk>/update/ajax', views.customer_purchases_update_ajax, name='purchases_update_ajax'),


]
