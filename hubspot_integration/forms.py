from django import forms
from .models import HubspotUser

class HubspotUserForm(forms.ModelForm):
    class Meta:
        model = HubspotUser
        fields = ['firstname', 'lastname', 'email']
