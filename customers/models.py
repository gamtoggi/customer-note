from django.db import models
from datetime import datetime
import calendar

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

    def get_contacts(self):
        return self.contact_set.order_by('-contacted_at', '-updated_at')

    def get_purchases(self):
        return self.purchase_set.order_by('-purchase_date', '-created_at')

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


    def get_waiting_next_purchases(self):
        return self.purchase_set \
                    .filter(next_purchase_date__isnull=False,
                            is_repurchased=False) \
                    .order_by('next_purchase_date')


    def get_address(self):
        str = '';
        if self.address1 != None:
            str += self.address1
        if self.address2 != None:
            str += ' ' + self.address2
        return str


    def get_month_purchases(self):
        year = datetime.now().year
        mon = datetime.now().month
        return self.purchase_set.filter(purchase_date__year=year, purchase_date__month=mon)


    def get_month_revenue(self):
        purchases = self.get_month_purchases()
        revenue = 0
        for p in purchases:
            revenue += p.get_total_price()
        return revenue


    def get_total_revenue(self):
        purchases = self.purchase_set.all()
        revenue = 0
        for p in purchases:
            revenue += p.get_total_price()
        return revenue


    @classmethod
    def order_by_name(cls, user_id):
        return cls.objects.filter(user_id=user_id).order_by('name')

    @classmethod
    def order_by_created_at(cls, user_id):
        return cls.objects.filter(user_id=user_id).order_by('-created_at')


    @classmethod
    def order_by_comming_next_purchase(cls, user_id):
        query = '''
            select customers_customer.id
            from customers_customer
            left join (
                select
                    customers_purchase.customer_id,
                    min(customers_purchase.next_purchase_date) as next_purchase_date
                from customers_purchase
                where
                    customers_purchase.user_id={user_id} and
                    customers_purchase.next_purchase_date is not null and
                    customers_purchase.is_repurchased=0
                group by customers_purchase.customer_id
            ) customers_purchase
            on customers_customer.id=customers_purchase.customer_id
            where customers_customer.user_id={user_id}
            order by
                customers_purchase.next_purchase_date is null,
                customers_purchase.next_purchase_date asc,
                customers_customer.name;
        '''.format(user_id=user_id)

        return cls.objects.raw(query)


    @classmethod
    def order_by_total_revenue(cls, user_id):
        query = cls.get_order_by_revenue_query(user_id, use_month_filter=False)
        return cls.objects.raw(query)


    @classmethod
    def order_by_month_revenue(cls, user_id):
        query = cls.get_order_by_revenue_query(user_id, use_month_filter=True)
        return cls.objects.raw(query)


    @classmethod
    def get_order_by_revenue_query(cls, user_id, use_month_filter):
        if use_month_filter:
            now = datetime.now()
            start_day, end_day = calendar.monthrange(now.year, now.month)
            start = '{0:04d}-{1:02d}-{2:02d}'.format(now.year, now.month, start_day)
            end = '{0:04d}-{1:02d}-{2:02d}'.format(now.year, now.month, end_day)

            month_filter = '''
                and customers_purchase.purchase_date >= '{start}'
                and customers_purchase.purchase_date <= '{end}'
            '''.format(start=start, end=end)
        else:
            month_filter = ''

        return '''
            select customers_customer.id
            from customers_customer
            left join (
              select customers_purchase.customer_id, sum(customers_purchase.unit_price * customers_purchase.count) as price
              from customers_purchase
              where customers_purchase.user_id={user_id} {month_filter}
              group by customers_purchase.customer_id
            ) customers_purchase
            on customers_customer.id=customers_purchase.customer_id
            where customers_customer.user_id={user_id}
            order by customers_purchase.price desc, customers_customer.name;
        '''.format(user_id=user_id, month_filter=month_filter)


    @classmethod
    def order_by_old_contact(cls, user_id):
        query = '''
            select customers_customer.id
            from customers_customer
            left join (
              select customers_contact.customer_id, max(customers_contact.contacted_at) as contacted_at
              from customers_contact
              where customers_contact.user_id={user_id}
              group by customers_contact.customer_id
            ) customers_contact
            on customers_customer.id=customers_contact.customer_id
            where customers_customer.user_id={user_id}
            order by customers_contact.contacted_at is null, customers_contact.contacted_at, customers_customer.name;
        '''.format(user_id=user_id)

        return cls.objects.raw(query)



class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contacted_at = models.DateField(default=datetime.now)
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

    def get_next_purchase_progress(self):
        if self.next_purchase_date != None and self.is_repurchased == False:
            max = (self.next_purchase_date - self.purchase_date).days
            value = (self.next_purchase_date - datetime.now().date()).days
            return { 'max': max, 'value': value }
        else:
            return None


    def get_next_purchase_progress_max(self):
        progress = self.get_next_purchase_progress()
        if progress != None:
            return progress['max']
        else:
            return None


    def get_next_purchase_progress_value(self):
        progress = self.get_next_purchase_progress()
        if progress != None:
            return progress['value']
        else:
            return None
