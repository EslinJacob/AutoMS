from django.urls import path

from .views import (
    mechanic_home,
    update_order,
)


app_name = 'mechanic'

urlpatterns = [
    path('', mechanic_home, name='mechanic_home'),
    path('<uuid:pk>/update/', update_order, name='update_order'),
]
