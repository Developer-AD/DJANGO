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


class MyUserAdmin(UserAdmin):
    model = MyUser

    # list_display = ['username', 'first_name', 'role']
    fieldsets = (
        ('Username & Password', {"fields": ('username', 'password', 'role')}),
        ('Extra Fields', {
            "fields": ('first_name', 'last_name', 'gender'),
        }),
        ('permissions', {
            "fields": (
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

# Register your models here.
# admin.site.register(MyUser, UserAdmin)
# admin.site.register(MyUser, CustomAdmin)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Student)
admin.site.register(DemoFiles)