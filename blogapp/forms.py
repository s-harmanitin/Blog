from django import forms
from .models import blog
from django.forms.widgets import TextInput,EmailInput,NumberInput,DateInput

class blogform(forms.ModelForm):
    class Meta:
        model = blog
        fields = "__all__"
        
        
    def __init__(self,*args,**kwargs):
        super(blogform,self).__init__(*args,**kwargs)
        self.fields['tag'].empty_label = "select tag"


        


