from django import forms
from .models import CustomUser

class SignupForm(forms.ModelForm):
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'autocomplete': 'new-password'
        }),
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'cellphone_number', 'country', 'planet', 'birth_date', 'genre']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'astronaut@galaxy.space',
                'autocomplete': 'email',
                'required': True
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'cosmic_explorer',
                'maxlength': '150',
                'autocomplete': 'username',
                'required': True
            }),
            'cellphone_number': forms.TextInput(attrs={
                'placeholder': '+1 234 567 8900',
                'maxlength': '20',
                'type': 'tel',
                'autocomplete': 'tel'
            }),
            'country': forms.TextInput(attrs={
                'placeholder': 'USA, Mexico, Spain...',
                'maxlength': '100',
                'autocomplete': 'country-name'
            }),
            'planet': forms.TextInput(attrs={
                'placeholder': 'Earth, Mars, Venus...',
                'maxlength': '100'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'autocomplete': 'bday'
            }),
            'genre': forms.Select(choices=[
                ('', 'Select...'),
                ('Male', 'Male'),
                ('Female', 'Female'),
                ('Alien', 'Alien')
            ])
        }
    
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        
        # Add custom CSS classes to all fields
        for field_name, field in self.fields.items():
            # Get existing classes or create empty string
            existing_classes = field.widget.attrs.get('class', '')
            
            # Add form-control class for consistent styling
            field.widget.attrs['class'] = existing_classes
            
            # Mark required fields
            if field.required:
                field.label = f"{field.label}"


class LoginForm(forms.Form):
    
    username = forms.CharField(
        label='Username or Email',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'cosmic_explorer or astronaut@galaxy.space',
            'autocomplete': 'username'
        })
    )
    
    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
            'autocomplete': 'current-password'
        })
    )