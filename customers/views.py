from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .models import Customer
from .forms import CustomerForm, CustomerNameForm, CustomerPhoneForm, CustomerKakaoForm, CustomerAddressForm, CustomerBirthdayForm, CustomerMemoForm


@login_required
def customer_list(request):
    context = get_customer_list_context()
    return render(request, 'customers/list.html', context)


@login_required
def customer_ajax_list(request):
    data = {}
    context = get_customer_list_context()
    data['html'] = render_to_string('customers/partial_list.html',
        context,
        request=request
    )
    return JsonResponse(data)


@login_required
def customer_detail(request, pk):
    context = get_customer_detail_context(pk, 'info')
    return render(request, 'customers/detail.html', context)


@login_required
def customer_ajax_detail(request, pk):
    context = get_customer_detail_context(pk, 'info')
    data = {}
    data['html'] = render_to_string('customers/partial_detail.html',
        context,
        request=request
    )
    return JsonResponse(data)


@login_required
def customer_ajax_create(request):
    '''ajax json api. 고객 추가'''
    data = {}
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            context = get_customer_list_context()
            data['result'] = 'ok'
            data['html'] = render_to_string('customers/partial_list_contents.html',
                context,
                request=request
            )
        else:
            data['result'] = 'fail'
            data['errors'] = form.errors
    elif request.method == 'GET':
        data['html'] = render_to_string('customers/form_modal.html',
            {},
            request=request
        )
    return JsonResponse(data)


@login_required
def customer_ajax_update(request, pk):
    data = {}
    status = 200
    if request.method == 'POST':
        customer = get_object_or_404(Customer, pk=pk)

        if request.POST.get('name') != None:
            form_class = CustomerNameForm
        elif request.POST.get('phone') != None:
            form_class = CustomerPhoneForm
        elif request.POST.get('kakao') != None:
            form_class = CustomerKakaoForm
        elif request.POST.get('address1') != None or request.POST.get('address2') != None:
            form_class = CustomerAddressForm
        elif request.POST.get('birthday') != None:
            form_class = CustomerBirthdayForm
        elif request.POST.get('memo') != None:
            form_class = CustomerMemoForm

        try:
            form = form_class(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                data['result'] = 'ok'
            else:
                data['result'] = 'fail'
                data['errors'] = form.errors
                status = 400
        except NameError:
            data['result'] = 'fail'
            data['errors'] = 'form is none'
            status = 400

    return JsonResponse(status=status, data=data)


def get_customer_list_context():
    context = {}
    context['customers'] = []
    object_list = Customer.objects.order_by('-created_at')
    for obj in object_list:
        context['customers'].append(obj.get_summary())
    context['customer_count'] = len(object_list)
    return context


def get_customer_detail_context(pk, tab_active):
    context = {}
    context['customer'] = get_object_or_404(Customer, pk=pk)
    context['tab_active'] = tab_active
    return context
