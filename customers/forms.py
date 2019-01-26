from django import forms
from .models import Customer, Contact

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
