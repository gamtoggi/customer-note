from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Customer, Contact
from . import forms


@login_required
def customer_list(request):
    context = get_customer_list_context()
    return render(request, 'customers/list/index.html', context)


@login_required
def customer_list_ajax(request):
    context = get_customer_list_context()
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
    context = get_customer_contacts_context(pk)
    return render(request, 'customers/detail/contacts/index.html', context)


@login_required
def customer_contacts_ajax(request, pk):
    context = get_customer_contacts_context(pk)
    return render_ajax_response(
        template='customers/detail/contacts/partial/contacts.html',
        context=context)


@login_required
def customer_contacts_create_ajax(request, pk):
    if request.method == 'GET':
        form = forms.ContactForm(initial={'contacted_at': timezone.now()})
        context = { 'form': form }

        return render_ajax_response(
                template='customers/detail/contacts/partial/form.html',
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
                template='customers/detail/contacts/partial/form.html',
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
    context = get_customer_purchases_context(pk)
    return render(request, 'customers/detail/purchases/index.html', context)


@login_required
def customer_purchases_ajax(request, pk):
    context = get_customer_purchases_context(pk)
    return render_ajax_response(
            template='customers/detail/purchases/partial/purchases.html',
            context=context)


def get_customer_list_context():
    context = {}
    context['customers'] = []
    object_list = Customer.objects.order_by('-created_at')
    for obj in object_list:
        context['customers'].append(obj.get_summary())
    context['customer_count'] = len(object_list)
    return context


def get_customer_info_context(pk):
    customer = get_object_or_404(Customer, pk=pk)
    return {
        'customer': customer,
        'tab_active': 'info',}
        # 'form': forms.CustomerUpdateForm(instance=customer) }


def get_customer_contacts_context(pk):
    customer = get_object_or_404(Customer,pk=pk)
    contacts = customer.contact_set.order_by('-contacted_at', '-updated_at')
    return {
        'customer': customer,
        'tab_active': 'contacts',
        'contacts': contacts,
        'contacts_count': customer.contact_set.count() }


def get_customer_purchases_context(pk):
    customer = get_object_or_404(Customer,pk=pk)

    return {
        'customer': customer,
        'tab_active': 'purchases', }


def render_ajax_response(template=None, request=None, context=None, status=200, errors=None):
    data = {}
    data['status'] = status
    if template != None:
        data['html'] = render_to_string(template, context, request=request)
    if errors != None:
        data['errors'] = errors
    return JsonResponse(data)
