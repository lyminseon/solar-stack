"""
URL configuration for solar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.home_page, name='login'),  # 로그인 페이지도 홈페이지 기반
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/check-auth/', views.check_auth, name='check_auth'),
    path('auth/', include('mozilla_django_oidc.urls')),
    path('admin/', admin.site.urls),
]

# 정적 파일 서빙 설정 (개발 환경)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# staticfiles 경로도 추가 (기존 HTML에서 사용하는 경로)
urlpatterns += static('/staticfiles/', document_root=settings.STATIC_ROOT)
