from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q

from .models import Customer, Contact, Purchase
from . import forms


@login_required
def customer_list(request):
    context = get_customer_list_context(request=request)
    return render(request, 'customers/list/index.html', context)


@login_required
def customer_list_ajax(request):
    context = get_customer_list_context(request=request)
    return render_ajax_response(
            template='customers/list/partial/list.html',
            context=context)


@login_required
def customer_create_ajax(request):
    if request.method == 'GET':
        return render_ajax_response(
                template='customers/list/partial/form.html',
                request=request)

    elif request.method == 'POST':
        form = forms.CustomerForm(request.POST)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            return customer_list_ajax(request)
        else:
            return render_ajax_response(status=400, errors=form.errors)


@login_required
def customer_update_ajax(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    field = request.GET.get('field')
    form_class = get_customer_partial_form_class(field)

    if request.method == 'GET':
        form = form_class(instance=customer)
        context = {'form': form, 'field': field}
        return render_ajax_response(
            template='customers/detail/info/partial/form.html',
            request=request,
            context=context)

    elif request.method == 'POST':
        form = form_class(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return customer_info_ajax(request, pk)
        else:
            return render_ajax_response(status=400, errors=form.errors)


def get_customer_partial_form_class(field):
    if field == 'name':
        form_class = forms.CustomerNameForm
    elif field == 'phone':
        form_class = forms.CustomerPhoneForm
    elif field == 'kakao':
        form_class = forms.CustomerKakaoForm
    elif field == 'address':
        form_class = forms.CustomerAddressForm
    elif field == 'birthday':
        form_class = forms.CustomerBirthdayForm
    elif field == 'memo':
        form_class = forms.CustomerMemoForm
    return form_class


@login_required
def customer_delete_ajax(request, pk):
    if request.method == 'GET':
        return render_ajax_response(
                template='customers/detail/info/partial/delete.html',
                request=request)


    elif request.method == 'POST':
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return redirect('customers:list_ajax')


@login_required
def customer_info(request, pk):
    context = get_customer_info_context(pk)
    return render(request, 'customers/detail/info/index.html', context)


@login_required
def customer_info_ajax(request, pk):
    context = get_customer_info_context(pk)
    return render_ajax_response(
            template='customers/detail/info/partial/info.html',
            context=context)


@login_required
def customer_contacts(request, pk):
    context = get_customer_contacts_context(request, pk)
    return render(request, 'customers/detail/contacts/index.html', context)


@login_required
def customer_contacts_ajax(request, pk):
    context = get_customer_contacts_context(request, pk)
    return render_ajax_response(
        template='customers/detail/contacts/partial/contacts.html',
        context=context)


@login_required
def customer_contacts_create_ajax(request, pk):
    if request.method == 'GET':
        form = forms.ContactForm(initial={'contacted_at': datetime.now()})
        context = { 'form': form }

        return render_ajax_response(
                template='customers/detail/contacts/partial/create_form.html',
                request=request,
                context=context)

    elif request.method == 'POST':
        form = forms.ContactForm(request.POST)

        if form.is_valid():
            customer = get_object_or_404(Customer, pk=pk)
            contact = form.save(commit=False)
            contact.user = request.user
            contact.customer = customer
            contact.save()
            return redirect('customers:contacts_ajax', pk=pk)
        else:
            return render_ajax_response(status=400, errors=form.errors)


@login_required
def customer_contacts_update_ajax(request, pk, contact_pk):
    contact = get_object_or_404(Contact, pk=contact_pk)

    if request.method == 'GET':
        form = forms.ContactForm(instance=contact)
        context = { 'form': form }
        return render_ajax_response(
                template='customers/detail/contacts/partial/update_form.html',
                request=request,
                context=context)

    elif request.method == 'POST':
        form = forms.ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('customers:contacts_ajax', pk=pk)
        else:
            return render_ajax_response(status=400, errors=form.errors)



@login_required
def customer_purchases(request, pk):
    context = get_customer_purchases_context(request, pk)
    return render(request, 'customers/detail/purchases/index.html', context)


@login_required
def customer_purchases_ajax(request, pk):
    context = get_customer_purchases_context(request, pk)
    return render_ajax_response(
            template='customers/detail/purchases/partial/purchases.html',
            context=context,
            request=request)


@login_required
def customer_purchases_create_ajax(request, pk):
    if request.method == 'GET':
        form = forms.PurchaseForm()
        context = { 'form': form }

        return render_ajax_response(
                template='customers/detail/purchases/partial/create_form.html',
                request=request,
                context=context)

    elif request.method == 'POST':
        form = forms.PurchaseForm(request.POST)

        if form.is_valid():
            customer = get_object_or_404(Customer, pk=pk)
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.customer = customer
            purchase.save()
            return redirect('customers:purchases_ajax', pk=pk)
        else:
            return render_ajax_response(status=400, errors=form.errors)


@login_required
def customer_purchases_update_ajax(request, pk, purchase_pk):
    purchase = get_object_or_404(Purchase, pk=purchase_pk)

    if request.method == 'GET':
        form = forms.PurchaseForm(instance=purchase)
        context = { 'form': form }
        return render_ajax_response(
                template='customers/detail/purchases/partial/update_form.html',
                request=request,
                context=context)

    elif request.method == 'POST':
        if request.GET.get('form_for') == 'is_repurchased':
            form_class = forms.PurchaseIsRepurchasedForm
        else:
            form_class = forms.PurchaseForm
        form = form_class(request.POST, instance=purchase)

        if form.is_valid():
            form.save()
            return redirect('customers:purchases_ajax', pk=pk)
        else:
            return render_ajax_response(status=400, errors=form.errors)


def get_customer_list_context(request):
    order = request.GET.get('order')
    if order == None:
        order = 'name'

    if order == 'create':
        customers =  Customer.objects.filter(user=request.user).order_by('-created_at')
    elif order == 'contact':
        customers = Customer.order_by_old_contact(request.user.id)
    elif order == 'next_purchase':
        customers = Customer.get_next_purchase_order_customers(request.user.id)
    elif order == 'total_revenue':
        customers = Customer.order_by_total_revenue(request.user.id)
    elif order == 'month_revenue':
        customers = Customer.order_by_month_revenue(request.user.id)
    else:
        customers = Customer.objects.filter(user=request.user).order_by('name')

    search = request.GET.get('search')
    if search != None:
        customers = customers.filter(Q(name__contains=search) | Q(address1__contains=search) | Q(address2__contains=search) | Q(memo__contains=search))

        for customer in customers:
            if customer.name.find(search) >= 0:
                customer.search_name = customer.name
            elif customer.address1 != None and customer.address1.find(search) >= 0:
                customer.search_match = customer.get_address()
            elif customer.address2 != None and customer.address2.find(search) >= 0:
                customer.search_match = customer.get_address()
            elif customer.memo != None and customer.memo.find(search) >= 0:
                customer.search_match = customer.memo

            if hasattr(customer, 'search_name'):
                customer.search_name = customer.search_name.replace(search, '<mark>' + search + '</mark>')
            elif hasattr(customer, 'search_match'):
                customer.search_match = customer.search_match.replace(search, '<mark>' + search + '</mark>')


    return {
        'order': order,
        'search': search,
        'customers': customers,
        'customer_count': len(customers) }


def get_customer_info_context(pk):
    customer = get_object_or_404(Customer, pk=pk)
    return {
        'customer': customer,
        'tab_active': 'info' }


def get_customer_contacts_context(request, pk):
    customer = get_object_or_404(Customer,pk=pk)
    contacts = customer.contact_set.order_by('-contacted_at', '-updated_at')

    search = request.GET.get('search')
    if search != None:
        contacts = contacts.filter(memo__contains=search)

    return {
        'customer': customer,
        'tab_active': 'contacts',
        'contacts': contacts,
        'contacts_count': customer.contact_set.count(),
        'search': search }


def get_customer_purchases_context(request, pk):
    customer = get_object_or_404(Customer,pk=pk)
    purchases = customer.purchase_set.order_by('-purchase_date', '-created_at')

    search = request.GET.get('search')
    if search != None:
        purchases = purchases.filter(name__contains=search)

    return {
        'customer': customer,
        'tab_active': 'purchases',
        'purchases': purchases,
        'purchases_count': customer.purchase_set.count(),
        'month_revenue': customer.get_month_revenue(),
        'search': search }


def render_ajax_response(template=None, request=None, context=None, status=200, errors=None):
    data = {}
    data['status'] = status
    if template != None:
        data['html'] = render_to_string(template, context, request=request)
    if errors != None:
        data['errors'] = errors
    return JsonResponse(data)
