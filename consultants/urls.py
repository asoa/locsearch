from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.conf.urls import url
from rest_framework import routers
from django.conf.urls import include

# router = routers.DefaultRouter()
# router.register(r'consultant', views.ConsultantViewSet)

urlpatterns = [
    path('search/', views.search, name='search'),
    path('like', views.like, name='like'),
    url(
        r'^api/v1/consultant/(?P<pk>[0-9]+)$',
        views.get_delete_update_consultant,
        name='get_delete_update_consultant'
    ),
    url(
        r'^api/v1/consultant/$',
        views.get_post_consultant,
        name='get_post_consultant'
    )
]