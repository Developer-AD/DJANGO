from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # path('send-email/', views.send_email, name="send_email"),

    path('', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.login_page, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    # path('create/', views.create, name="create"),
    # path('delete/<int:id>/', views.delete),
    # path('edit/<int:id>/', views.edit),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
