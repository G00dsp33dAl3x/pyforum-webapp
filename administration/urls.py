from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Login logic
    path('administrator/', views.logon_admin, name='admin_panel'),
    path('administrator/info/', login_required(views.info), name='info'),
    path('administrator/logout/', auth_views.LogoutView.as_view(next_page='admin_panel'), name='logout'),
    path('administrator/approve_company/', login_required(views.approve_company), name='approve_company'),
    path('administrator/approve_company/erdpou/<int:id>/', login_required(views.erdpou_aproved), name='erdpou_aproved'),
    path('administrator/approve_company/unregistered/<int:id>/', login_required(
        views.company_unregistered), name='company_unregistered'
        ),
    path('administrator/company/<int:id>/', login_required(views.admin_full_company_info), name='admin_full_company_info'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
