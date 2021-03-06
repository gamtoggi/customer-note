from django import forms
from .models import Customer, Contact, Purchase

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'phone', 'kakao', 'address1', 'address2', 'birthday', 'memo')


class CustomerNameForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name',)


class CustomerPhoneForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('phone',)


class CustomerKakaoForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('kakao',)


class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('address1', 'address2')


class CustomerBirthdayForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('birthday',)


class CustomerMemoForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('memo',)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('contacted_at', 'memo',)


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = (
                'name',
                'count',
                'unit_price',
                'purchase_date',
                'next_purchase_date',
                'is_repurchased', )


class PurchaseIsRepurchasedForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('is_repurchased', )


def get_customer_partial_form_class(field):
    if field == 'name':
        return CustomerNameForm
    elif field == 'phone':
        return CustomerPhoneForm
    elif field == 'kakao':
        return CustomerKakaoForm
    elif field == 'address':
        return CustomerAddressForm
    elif field == 'birthday':
        return CustomerBirthdayForm
    elif field == 'memo':
        return CustomerMemoForm
    return None
