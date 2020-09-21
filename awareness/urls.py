"""type2beat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from awareness import views as awareness_views

urlpatterns = [
    url(r'^$', awareness_views.index, name='home'),
    url(r'^contacts/', awareness_views.contacts, name='contacts'),
    url(r'^exercises/', awareness_views.exercises, name='exercises'),
    url(r'^healthy_diets/', awareness_views.healthy_diets, name='healthy_diets'),
    url(r'^prevention/', awareness_views.prevention, name='prevention'),
    url(r'^services/', awareness_views.services, name='services'),
    url(r'^water/', awareness_views.water, name="water"),
    url(r'^fast/', awareness_views.fast, name="fast"),
    url(r'^diabetes/', awareness_views.diabetes, name="diabetes"),
    url(r'^impact', awareness_views.impact,name='impact'),
    url(r'^heart', awareness_views.heart,name='heart'),
    url(r'^eyes', awareness_views.eyes,name="eyes"),
    url(r'^kidney', awareness_views.kidney,name="kidney"),
    url(r'^nerves', awareness_views.nerves,name='nerves'),
    url(r'^digestion',awareness_views.digestion,name ='digestion'),
    url(r'^skin',awareness_views.skin,name='skin'),
    url(r'^conditions', awareness_views.conditions,name='conditions'),
    url(r'^privacy/', awareness_views.privacy, name='privacy'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
