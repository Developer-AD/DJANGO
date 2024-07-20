from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # path('send-email/', views.send_email, name="send_email"),

    path('', views.dashboard, name="dashboard"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_page, name="logout"),

# ----------------------- Student routes -----------------------
    path('student-add/', views.student_add, name="student_add"),
    path('student-edit/<int:id>/', views.student_edit,),
    path('student-delete/<int:id>/', views.student_delete),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
