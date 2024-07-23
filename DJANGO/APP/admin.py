from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Student, DemoFiles

# class CustomAdmin(admin.ModelAdmin):
#     list_display = ('username', 'role', 'first_name')
#     list_per_page = 10
#     search_fields = ('username',)
#     ordering = ('role','username')  # ('-username',)
#     list_filter = ('username',)
#     # readonly_fields = ('username', 'password',) # We can change username field. we use so that we don't.
#     # prepopulated_fields = #



# Register your models here.
# admin.site.register(MyUser, CustomAdmin)
admin.site.register(MyUser, UserAdmin)
admin.site.register(Student)
admin.site.register(DemoFiles)