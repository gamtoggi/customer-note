from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .models import Customer
from .forms import CustomerForm, CustomerNameForm, CustomerPhoneForm, CustomerKakaoForm, CustomerAddressForm, CustomerBirthdayForm, CustomerMemoForm


@login_required
def customer_index(request):
    '''고객 목록 full 페이지'''
    context = get_customer_list_context()
    return render(request, 'customers/index.html', context)


@login_required
def customer_list(request):
    '''ajax용으로 navbar 등을 제외한 고객 리스트 부분만 전송'''
    data = {}
    context = get_customer_list_context()
    data['html'] = render_to_string('customers/list.html',
        context,
        request=request
    )
    return JsonResponse(data)


@login_required
def customer_detail(request, pk):
    '''ajax용으로 navbar 등을 제외한 고객 정보 페이지만 전송'''
    data = {}
    context = {}
    context['customer'] = get_object_or_404(Customer, pk=pk)
    context['tab_active'] = 'info'
    data['html'] = render_to_string('customers/detail.html',
        context,
        request=request
    )
    # return render(request, 'customers/detail.html', context)
    return JsonResponse(data)


@login_required
def customer_create(request):
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
            data['html'] = render_to_string('customers/partial_list.html',
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
def customer_update(request, pk):
    '''ajax json api. 고객 정보 수정'''
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
    '''고객 목록 페이지에 필요한 정보를 dictionary 형태로 반환'''
    context = {}
    context['customers'] = []
    object_list = Customer.objects.order_by('-created_at')
    for obj in object_list:
        context['customers'].append(obj.get_summary())
    context['customer_count'] = len(object_list)
    return context
