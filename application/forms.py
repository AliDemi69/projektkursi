# accounts/forms.py
from django import forms 
from django.contrib.auth import get_user_model

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def create(self):
        User = get_user_model()
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        return user
    

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'password')

# Search

class SearchForm(forms.Form):
    query = forms.CharField(label='Search')

class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email')
    address = forms.CharField(label='Address', widget=forms.Textarea)
    city = forms.CharField(label='City', max_length=100)
    postal_code = forms.CharField(label='Postal Code', max_length=10)
    country = forms.CharField(label='Country', max_length=100)
    payment_method = forms.ChoiceField(label='Payment Method', choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
    card_number = forms.CharField(label='Card Number', max_length=16, required=False)
    expiration_date = forms.CharField(label='Expiration Date (MM/YY)', max_length=5, required=False)
    cvv = forms.CharField(label='CVV', max_length=4, required=False)
