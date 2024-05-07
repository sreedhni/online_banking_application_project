"""
URL configuration for bankproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.schemas import get_schema_view

# schema_view = get_schema_view(title='EMS API Documentation')
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/user/', include('account.urls')),
#     path('staff/', include('Staff.urls')),
#     path('customer/', include('Customer.urls')),
#     path('api_documentation/', schema_view),  # Add trailing slash and use path()
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="EMS API Documentation",
        default_version='v1',
        description="Documentation for EMS API",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),
    path('staff/', include('Staff.urls')),
    path('customer/', include('Customer.urls')),
    path('api_documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('financialplan/', include('FinancialPlanningTools.urls')),

]


