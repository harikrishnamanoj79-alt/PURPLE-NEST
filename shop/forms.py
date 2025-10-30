# forms.py
# ----------------------------------------------
# All User, Admin, and Delivery Forms
# ----------------------------------------------

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Review, ContactMessage, Product, Category, DeliveryTracking, Order


# ======================================================
# 1️⃣ USER REGISTRATION FORM
# ======================================================
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'form-control'
        })
    )
    phone = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone Number',
            'class': 'form-control'
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Address',
            'rows': 2,
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'phone', 'address', 'password1', 'password2'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name',
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name',
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'form-control'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm Password',
                'class': 'form-control'
            }),
        }


# ======================================================
# 2️⃣ LOGIN FORM
# ======================================================
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username or Email',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        })
    )


# ======================================================
# 3️⃣ CONTACT FORM
# ======================================================
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email',
                'class': 'form-control'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject',
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Your Message',
                'rows': 4,
                'class': 'form-control'
            }),
        }


# ======================================================
# 4️⃣ REVIEW FORM
# ======================================================
class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, '⭐' * i) for i in range(1, 6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your review...',
                'rows': 3,
                'class': 'form-control'
            }),
        }


# ======================================================
# 5️⃣ PRODUCT FORM (ADMIN)
# ======================================================
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image', 'stock', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Product Name',
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Price',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Product Description',
                'rows': 3,
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={
                'placeholder': 'Stock Quantity',
                'class': 'form-control'
            }),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ======================================================
# 6️⃣ CATEGORY FORM (ADMIN)
# ======================================================
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Category Name',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Category Description',
                'rows': 2,
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ======================================================
# 7️⃣ DELIVERY STATUS FORM (DELIVERY STAFF)
# ======================================================
class DeliveryStatusForm(forms.ModelForm):
    class Meta:
        model = DeliveryTracking
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Optional notes...',
                'rows': 2,
                'class': 'form-control'
            }),
        }


# ======================================================
# 8️⃣ ORDER STATUS FORM (ADMIN)
# ======================================================
class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image', 'stock', 'is_featured']
