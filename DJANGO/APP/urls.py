from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # path('send-email/', views.send_email, name="send_email"),

    path('', views.home, name="home"),
    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),
    path('login/', views.Login.as_view(), name="login"),
    path('register/', views.Register.as_view(), name="register"),
    path('logout/', views.logout_page, name="logout"),

# ----------------------- Student routes -----------------------
    path('student-add/', views.student_add, name="student_add"),
    path('student-edit/<int:id>/', views.student_edit),
    path('student-delete/<int:id>/', views.student_delete),

# ----------------------- New routes --------------------------
    path('send-email/', views.send_email_attachment, name='send_email'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
