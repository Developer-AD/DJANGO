from django.contrib import admin
from .models import MyUser, Student, DemoFiles

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Student)
admin.site.register(DemoFiles)