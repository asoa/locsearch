from django.urls import path
from django.conf.urls.static import static
from django.urls import include
from django.conf import settings
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # path('blog/', views.index, name='blog'),
    path('blog/<int:pk>/', views.post, name='post_detail'),
    path('blog/', views.blog, name='blog'),
    path('markdownx/', include('markdownx.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)