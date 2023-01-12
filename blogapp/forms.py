from django import forms
from .models import blog
from django.forms.widgets import TextInput,EmailInput,NumberInput,DateInput
# from phonenumber_field.formfields import PhoneNumberField

class blogform(forms.ModelForm):
    class Meta:
        model = blog
        fields = "__all__"
        
        
    def __init__(self,*args,**kwargs):
        super(blogform,self).__init__(*args,**kwargs)
        self.fields['tag'].empty_label = "select tag"

# class PhoneForm(forms.Form):
#     number = PhoneNumberField(region="IN")


