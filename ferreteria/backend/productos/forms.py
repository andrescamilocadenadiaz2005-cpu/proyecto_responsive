from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'email', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
<<<<<<< HEAD
        }
=======
        }
        
>>>>>>> bc0ef0a471e8a2a5db0b0ffdc6e73de6f5fc9b1e
