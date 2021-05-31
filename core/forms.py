from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
import django_filters
from django_filters import DateFilter
from allauth.account.forms import SignupForm

PAYMENT_CHOICES = (
    ('Gcash', 'Gcash'),
    ('Cash on Delivery', 'Cash on Delivery')
)

class CreateUserForm(UserCreationForm):
    contact = forms.IntegerField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class PostForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['user', 'store', 'slug']

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['slug']

class ItemFormTwo(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['slug','user','store']

class OthersForm(ModelForm):
    note = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your sugo. (Complete Details)'
    }))
    class Meta:
        model = Order
        fields = 'note',
        exclude = ['user']

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class ChoiceForm(forms.Form):
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class SearchOrderForm(forms.ModelForm):
    ordered_date = forms.DateTimeField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'YYYY-MM-DD'
        }))
 
    class Meta:
        model = Order
        fields = ['date_ordered']

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_ordered", lookup_expr='gte', widget=forms.TextInput(attrs={
        'placeholder': 'YYYY-MM-DD'
        }))
    end_date = DateFilter(field_name="date_ordered", lookup_expr='lte', widget=forms.TextInput(attrs={
        'placeholder': 'YYYY-MM-DD'
        }))

    class Meta:
       model = Order
       fields = '__all__'
       exclude = ['user', 'ref_code', 'date_ordered', 'items', 'ordered', 'shipping_address', 'payment', 'service_charge', 'total', 'being_delivered', 'received', 'rider', 'other', 'status']

######################### ADMIN ##########################

class AdminForm(ModelForm):
    email = forms.CharField(required=False)
    profile_pic = forms.ImageField(label='Profile Picture', required=True)
    class Meta:
        model = Admin
        fields = 'profile_pic','first_name','middle_name','last_name','suffix','gender','email','contact'
        exclude = ['user',]

class AdminForm1(ModelForm):
    class Meta:
        model = Admin
        fields = 'is_active',

class EditRiderForm(ModelForm):
    class Meta:
        model = Rider
        fields = 'is_active',

class EditPartnerForm(ModelForm):
    class Meta:
        model = PartnerStore
        fields = 'is_active',

class PartnerForm(ModelForm):
    class Meta:
        model = PartnerStore
        fields = 'category','store','profile_pic','first_name','last_name','middle_name','suffix','gender','contact','email'
        exclude = ['user']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = 'title','is_active'

class ShippingRateForm(ModelForm):
    class Meta:
        model = Rate
        fields = '__all__'

        labels = {
            "shipping_rate":"Shipping Rate (Per km)",
        }

class DistanceCalculatorForm(ModelForm):
    class Meta:
        model = PartnerStore
        fields = 'store',

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = 'rider', 'status', 'service_charge', 'surcharge'

        exclude = ['user']

        labels = {
            "rider":"Rider",
            "status":"status",
            "service_charge":"Service Charge:",
            "surcharge":"Surcharge"
            }

######################### CUSTOMER ##########################

class CustomerForm(ModelForm):
    profile_pic = forms.ImageField(required=True, label="Profile Picture")
    class Meta:
        model = Customer
        fields = 'profile_pic','first_name','middle_name','last_name','suffix','gender','contact','email'
        exclude = ['user']

class UploadSignUpForm(ModelForm):
    profile_pic = forms.ImageField(required=True, label="Photo of your face")
    validid_pic = forms.ImageField(required=True, label="Photo of your valid ID")
    faceid_pic = forms.ImageField(required=True, label="Photo of yourself holding your ID")
    class Meta:
        model = Customer
        fields = ('profile_pic','validid_pic','faceid_pic','is_active')

class VerificationSignUpForm(ModelForm):
    contact = forms.IntegerField(label='', required=False)
    temp = forms.IntegerField(label='', required=False)
    class Meta:
        model = Customer
        fields = 'contact',
        
class SignUpForm(ModelForm):
    class Meta:
        model = Customer
        fields = 'profile_pic',
        exclude = ['user','first_name','last_name','middle_name','contact']

        labels = {
            "profile_pic":"Profile picture"
            }

######################### CUSTOMER ##########################

######################### DISPATCHER ##########################

class dis(ModelForm):
    class Meta:
        model = Dispatcher
        fields = '__all__'

class ProUpsSignUpFormDispatch(ModelForm):
    profile_pic = forms.ImageField(label='Photo of your face', required=True)
    class Meta:
        model = Dispatcher
        fields = 'profile_pic',

class DispatcherForm(ModelForm):
    profile_pic = forms.ImageField(label='Profile picture', required=True)
    class Meta:
        model = Dispatcher
        fields = 'profile_pic','first_name','middle_name','last_name','suffix','gender','contact','email'
        exclude = ['user']

class EditDisForm(ModelForm):
    class Meta:
        model = Dispatcher
        fields = 'is_active',

######################### DISPATCHER ##########################

######################### RIDER ##########################

class ProUpsSignUpFormRider(ModelForm):
    profile_pic = forms.ImageField(label='Photo of your face', required=True)
    class Meta:
        model = Rider
        fields = 'profile_pic',

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = 'rider', 'status', 'service_charge', 'surcharge'

        exclude = ['user']

        labels = {
            "rider":"Rider",
            "status":"status",
            "service_charge":"Service Charge:",
            "surcharge":"Surcharge"
            }

class RiderOrderStatusForm(ModelForm):
    class Meta:
        model = Order
        fields = 'status',

        exclude = ['user']

        labels = {
            "status":"Status"
            }

class RiderForm(ModelForm):
    profile_pic = forms.ImageField(label='Profile Picture', required=True)
    class Meta:
        model = Rider
        fields = 'profile_pic','first_name','last_name','middle_name','suffix','gender','contact','email','status'
        exclude = ['user']

class RiderStatusForm(ModelForm):
    class Meta:
        model = Rider
        fields = 'status',
        exclude = ['user']

        labels = {
            "status":"Status"
            }

######################### RIDER ##########################

######################### PARTNERSTORE ##########################

######################### PARTNERSTORE ##########################