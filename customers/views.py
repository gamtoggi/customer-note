from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .models import Customer
from .forms import CustomerForm


@login_required
def customer_index(request):
    context = get_customer_list_context()
    return render(request, 'customers/index.html', context)


@login_required
def customer_list(request):
    data = {}

    context = get_customer_list_context()
    data['html'] = render_to_string('customers/list.html',
        context,
        request=request
    )
    return JsonResponse(data)


@login_required
def customer_detail(request, pk):
    data = {}

    context = {}
    context['customer'] = get_object_or_404(Customer, pk=pk)

    data['html'] = render_to_string('customers/detail.html',
        context,
        request=request
    )
    # return render(request, 'customers/detail.html', context)
    return JsonResponse(data)


@login_required
def customer_create(request):
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


def get_customer_list_context():
    context = {}
    context['customers'] = []

    object_list = Customer.objects.order_by('-created_at')
    for obj in object_list:
        context['customers'].append(obj.get_summary())

    context['customer_count'] = len(object_list)

    return context
