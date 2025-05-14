from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import User, Moodboard, ContactMessage

#Moodboard form-------------------------------
class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Register as")
    speciality = forms.ChoiceField(choices=User.Categories, required=False, label="Speciality")
    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2","speciality","profile_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Custom layout for the form
       

#Moodboard form-------------------------------
class MoodboardForm(forms.ModelForm):
	class Meta:
		model = Moodboard
		fields = ['title','description','image','category','price']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_image','speciality']
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }
