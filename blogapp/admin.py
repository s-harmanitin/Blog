from django.contrib import admin

from .models import blog,tag,userdetails


# Register your models here.



admin.site.register(blog)
admin.site.register(tag)
admin.site.register(userdetails)

