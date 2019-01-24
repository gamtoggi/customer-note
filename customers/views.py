from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Customer
from .forms import CustomerForm


@login_required
def customer_list(request):
    context = get_customer_list_context()
    return render(request, 'customers/index.html', context)


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
