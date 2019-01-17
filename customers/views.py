from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

from .models import Customer


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    paginate_by = 100
    template_name = 'customers/index.html'


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ['name', 'phone', 'kakao', 'address1', 'address2', 'birthday', 'memo']
    template_name = 'customers/create_form.html'

    def get(self, request):
        html = render_to_string(self.template_name, {}, request=request)
        return JsonResponse({'html': html})