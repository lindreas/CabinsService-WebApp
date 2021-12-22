from django import forms

class NewOrderForm(forms.Form):
    cabins = forms.CharField(label="cabins", max_length=300)
    service = forms.CharField(label="service", max_length=100)
    order_date = forms.DateField(input_formats=['%Y-%m-%d'])
    selected_cabin = forms.IntegerField(label="selected_cabin", required=False)

class DeleteOrderForm(forms.Form):
    order = forms.IntegerField(label="order")

class LoginForm(forms.Form):
    email = forms.CharField(label="email", max_length=100)
    password = forms.CharField(label="password", widget=forms.PasswordInput())
