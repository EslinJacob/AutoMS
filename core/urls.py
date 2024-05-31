from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm

from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index_page'),
    path('signup/', views.signup, name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html',
            authentication_form=LoginForm
        ),
        name='login'
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('unauthorised/', views.unauthorised, name='unauthorised'),
    path('usermanagement/', views.user_mgmt, name='user_mgmt'),
    path('<int:pk>/edit/', views.edit_employee, name='edit_employee'),
    path('<int:pk>/delete/', views.delete_employee, name='delete_employee'),
]