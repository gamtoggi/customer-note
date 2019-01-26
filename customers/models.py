from django.db import models

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

    def get_summary(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'contact_ago': 0,
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
