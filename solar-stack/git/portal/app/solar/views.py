from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
import requests
from django.conf import settings

@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """Keycloak OIDC 로그인 리디렉션"""
    try:
        # Keycloak OIDC 로그인 URL로 리디렉션
        oidc_login_url = reverse('oidc_authentication_init')
        return JsonResponse({
            'success': True,
            'redirect_url': oidc_login_url,
            'message': 'Keycloak 로그인으로 리디렉션됩니다.'
        })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': '로그인 처리 중 오류가 발생했습니다.'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    """Keycloak OIDC 로그아웃"""
    try:
        # Django 로그아웃
        logout(request)
        # Keycloak 로그아웃 URL로 리디렉션
        oidc_logout_url = reverse('oidc_logout')
        return JsonResponse({
            'success': True, 
            'redirect_url': oidc_logout_url,
            'message': '로그아웃되었습니다.'
        })
    except Exception as e:
        request.session.flush()
        return JsonResponse({'success': True, 'message': '로그아웃되었습니다.'})

@require_http_methods(["GET"])
def check_auth(request):
    """인증 상태 확인 - Keycloak OIDC 기반"""
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else ''
    
    return JsonResponse({
        'authenticated': is_authenticated,
        'username': username,
        'email': request.user.email if is_authenticated else '',
        'first_name': request.user.first_name if is_authenticated else '',
        'last_name': request.user.last_name if is_authenticated else ''
    })

def home_page(request):
    """공개 홈페이지 - portal.html 템플릿 사용"""
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else '',
    }
    return render(request, 'portal.html', context)

def admin_dashboard(request):
    """관리자 대시보드 - 로그인 후 관리 도구 접근"""
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else '',
        'email': request.user.email if request.user.is_authenticated else '',
        'first_name': request.user.first_name if request.user.is_authenticated else '',
        'last_name': request.user.last_name if request.user.is_authenticated else '',
    }
    return render(request, 'portal.html', context)

# 하위 호환성을 위한 기존 함수 유지
def main_portal(request):
    """메인 포털 페이지 - 홈페이지로 리디렉션"""
    return home_page(request)

def integrated_dashboard(request):
    """통합 대시보드 - Airflow, MLflow 등을 iframe으로 내장"""
    context = {
        "is_authenticated": request.user.is_authenticated,
        "username": request.user.username if request.user.is_authenticated else "",
        "email": request.user.email if request.user.is_authenticated else "",
        "first_name": request.user.first_name if request.user.is_authenticated else "",
        "last_name": request.user.last_name if request.user.is_authenticated else "",
    }
    return render(request, "integrated_dashboard.html", context)
