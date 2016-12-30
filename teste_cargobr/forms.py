from django import forms


class AnatelUploadForm(forms.Form):
    file = forms.FileField(required=True)


class ConsultNumberForm(forms.Form):
    number = forms.CharField(max_length=10, required=True)
