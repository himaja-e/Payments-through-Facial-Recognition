from cProfile import label
from django  import forms

class upload(forms.Form):
    name = forms.CharField(label = "Enter username",max_length=250)

    password = forms.CharField(label="Enter password",max_length=30)

    file = forms.FileField(label="\nChoose file name same as user name")
    