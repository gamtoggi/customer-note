from django.db import models
from datetime import datetime

from users.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30, null=True, blank=True)
    kakao = models.CharField(max_length=30, null=True, blank=True)
    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '[{}] {} (owner : {})'.format(self.pk, self.name, self.user.username)


    def get_last_contact(self):
        queryset = self.contact_set.order_by('-contacted_at', '-updated_at')[:1]
        if queryset.count() > 0:
            return queryset[0]
        else:
            return None

    def get_last_contact_ago(self):
        last_contact = self.get_last_contact()
        if last_contact != None:
            delta = datetime.now().date() - last_contact.contacted_at
            return delta.days
        else:
            return -1


    def get_summary(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'contact_ago': self.get_last_contact_ago(),
        }

    def get_address(self):
        str = '';
        if self.address1 != None:
            str += self.address1
        if self.address2 != None:
            str += ' ' + self.address2
        return str


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contacted_at = models.DateField()
    memo = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '[{}] {}:{}'.format(self.pk, self.customer.name, self.memo)


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    count = models.PositiveSmallIntegerField(default=1)
    unit_price = models.PositiveSmallIntegerField(default=0)
    purchase_date = models.DateField(default=datetime.now)
    next_purchase_date = models.DateField(null=True, blank=True)
    is_repurchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '[{}] {}:{}'.format(self.pk, self.customer.name, self.name)

    def get_total_price(self):
        return self.count * self.unit_price
