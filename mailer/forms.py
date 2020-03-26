from django import forms
from .models import emailModel

class emailForm(forms.Form):
    email = forms.EmailField()
    subject= forms.CharField(max_length=100)
    cc=  forms.EmailField()
    bcc= forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class emailModelForm(forms.ModelForm):
    class Meta:
        model = emailModel
        fields = ['email', 'subject', 'cc', 'bcc', 'message']

