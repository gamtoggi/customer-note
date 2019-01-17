from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

from .models import Customer


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    paginate_by = 100
    template_name = 'customers/index.html'
