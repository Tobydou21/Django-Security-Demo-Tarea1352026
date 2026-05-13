from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # CSRF
    path('csrf/seguro/',     views.csrf_seguro,     name='csrf_seguro'),
    path('csrf/vulnerable/', views.csrf_vulnerable, name='csrf_vulnerable'),
    path('csrf/ataque/',     views.csrf_ataque,     name='csrf_ataque'),

    # XSS
    path('xss/seguro/',      views.xss_seguro,      name='xss_seguro'),
    path('xss/vulnerable/',  views.xss_vulnerable,  name='xss_vulnerable'),

    # Clickjacking
    path('clickjacking/seguro/',     views.clickjacking_seguro,     name='clickjacking_seguro'),
    path('clickjacking/vulnerable/', views.clickjacking_vulnerable, name='clickjacking_vulnerable'),
    path('clickjacking/ataque/',     views.clickjacking_ataque,     name='clickjacking_ataque'),
]