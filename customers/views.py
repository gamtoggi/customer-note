from datetime import datetime

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Customer, Contact, Purchase
from . import forms


@login_required
def customer_list(request):
    '''고객 목록 페이지'''
    context = get_customer_list_context(request=request)
    return render(request, 'customers/list/index.html', context)


@login_required
def customer_list_ajax(request):
    '''고객 목록 페이지 (Ajax)'''
    context = get_customer_list_context(request=request)
    return render_ajax_response(
            template='customers/list/partial/list.html',
            context=context)


@login_required
def customer_create_ajax(request):
    '''고객 생성 폼 처리 (Ajax)'''

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
    '''고객 수정 폼 처리 (Ajax)
    field 쿼리로 수정하고자 하는 정보 이름을 전달해야 한다.
    (고객 정보 중 이름, 전화, 주소 등 각각 따로 partial form으로 처리하기 위함)
    '''

    customer = get_my_object_or_error(request, Customer, pk)
    field = request.GET.get('field')
    form_class = forms.get_customer_partial_form_class(field)

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
            return redirect('customers:info_ajax', pk=pk)
        else:
            return render_ajax_response(status=400, errors=form.errors)


@login_required
def customer_delete_ajax(request, pk):
    '''고객 삭제 폼 처리 (Ajax)'''

    if request.method == 'GET':
        return render_ajax_response(
                template='customers/detail/info/partial/delete.html',
                request=request)


    elif request.method == 'POST':
        customer = get_my_object_or_error(request, Customer, pk)
        customer.delete()
        return redirect('customers:list_ajax')


@login_required
def customer_info(request, pk):
    '''고객 정보 페이지'''
    context = get_customer_info_context(request, pk)
    return render(request, 'customers/detail/info/index.html', context)


@login_required
def customer_info_ajax(request, pk):
    '''고객 정보 페이지 (Ajax)'''
    context = get_customer_info_context(request, pk)
    return render_ajax_response(
            template='customers/detail/info/partial/info.html',
            context=context)


@login_required
def customer_contacts(request, pk):
    '''고객 연락 정보 페이지'''
    context = get_customer_contacts_context(request, pk)
    return render(request, 'customers/detail/contacts/index.html', context)


@login_required
def customer_contacts_ajax(request, pk):
    '''고객 연락 정보 페이지 (Ajax)'''
    context = get_customer_contacts_context(request, pk)
    return render_ajax_response(
        template='customers/detail/contacts/partial/contacts.html',
        context=context)


@login_required
def customer_contacts_create_ajax(request, pk):
    '''고객 연락 정보 생성 폼 처리 (Ajax)'''

    if request.method == 'GET':
        context = { 'form': forms.ContactForm() }

        return render_ajax_response(
                template='customers/detail/contacts/partial/create_form.html',
                request=request,
                context=context)

    elif request.method == 'POST':
        form = forms.ContactForm(request.POST)

        if form.is_valid():
            customer = get_my_object_or_error(request, Customer, pk)
            contact = form.save(commit=False)
            contact.user = request.user
            contact.customer = customer
            contact.save()
            return redirect('customers:contacts_ajax', pk=pk)
        else:
            return render_ajax_response(status=400, errors=form.errors)


@login_required
def customer_contacts_update_ajax(request, pk, contact_pk):
    '''고객 연락 정보 수정 폼 처리 (Ajax)'''

    contact = get_my_object_or_error(request, Contact, contact_pk)

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
    '''고객 구입 정보 목록 페이지'''
    context = get_customer_purchases_context(request, pk)
    return render(request, 'customers/detail/purchases/index.html', context)


@login_required
def customer_purchases_ajax(request, pk):
    '''고객 구입 정보 목록 페이지 (Ajax)'''
    context = get_customer_purchases_context(request, pk)
    return render_ajax_response(
            template='customers/detail/purchases/partial/purchases.html',
            context=context,
            request=request)


@login_required
def customer_purchases_create_ajax(request, pk):
    '''고객 구입 정보 생성 폼 처리 (Ajax)'''

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
            customer = get_my_object_or_error(request, Customer, pk)
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.customer = customer
            purchase.save()
            return redirect('customers:purchases_ajax', pk=pk)
        else:
            return render_ajax_response(status=400, errors=form.errors)


@login_required
def customer_purchases_update_ajax(request, pk, purchase_pk):
    '''고객 구입 정보 수정 폼 처리 (Ajax)
    재구매 완료 정보만 업데이트 하는 경우 get query 의 form_for 값을 is_repurchased로 해야한다.
    '''

    purchase = get_my_object_or_error(request, Purchase, purchase_pk)

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


def get_from_param_or_session(request, key):
    value = request.GET.get(key)
    if value == None:
        value = request.session.get(key)

    if value != None:
        request.session[key] = value

    return value



def get_customer_list_context(request):
    '''고객 목록 context 반환
    order 쿼리값에 따라 고객 목록을 정렬하거나
    search 쿼리값에 따라 고객을 검색하여 고객 목록을 만든다.
    '''
    order = get_from_param_or_session(request, 'order')
    search = get_from_param_or_session(request, 'search')

    if search != None:
        customers = Customer.order_by_name(request.user.id).filter(
                        Q(name__contains=search) |
                        Q(address1__contains=search) |
                        Q(address2__contains=search) |
                        Q(memo__contains=search))
        customers = add_search_match_highlight_attr(customers, search)
    else:
        customers = get_ordered_customers(order, request.user.id)

    return {
        'order': order,
        'search': search,
        'customers': customers,
        'customer_count': len(customers) }


def get_ordered_customers(order, user_id):
    '''고객 목록 정렬'''
    if order == 'create':
        return Customer.order_by_created_at(user_id)
    elif order == 'contact':
        return Customer.order_by_old_contact(user_id)
    elif order == 'next_purchase':
        return Customer.order_by_comming_next_purchase(user_id)
    elif order == 'total_revenue':
        return Customer.order_by_total_revenue(user_id)
    elif order == 'month_revenue':
        return Customer.order_by_month_revenue(user_id)
    else:
        return Customer.order_by_name(user_id)


def add_search_match_highlight_attr(customers, search):
    '''고객 이름, 주소, 메모 등의 정보에 search 단어가 포함되어있으면
    template 에서 사용 가능한 search_name 이나 search_match attribute를 추가한다.
    '''
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

    return customers


def get_customer_info_context(request, pk):
    '''고객 정보 페이지에 필요한 context'''
    customer = get_my_object_or_error(request, Customer, pk)
    return {
        'customer': customer,
        'tab_active': 'info' }


def get_customer_contacts_context(request, pk):
    '''고객 연락 정보 페이지에 필요한 context'''
    customer = get_my_object_or_error(request, Customer, pk)
    contacts = customer.get_contacts()

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
    '''고객 구입 페이지에 필요한 context'''
    customer = get_my_object_or_error(request, Customer, pk)
    purchases = customer.get_purchases()

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
    '''Json 형태로 Ajax요청에 응답함'''
    data = {}
    data['status'] = status
    if template != None:
        data['html'] = render_to_string(template, context, request=request)
    if errors != None:
        data['errors'] = errors
    return JsonResponse(data, status=status)


def get_my_object_or_error(request, cls, pk):
    '''사용자가 생성한 고객 정보에만 접근 가능하도록 함'''
    object = get_object_or_404(cls, pk=pk)
    if object.user_id == request.user.id:
        return object;
    else:
        raise PermissionDenied
