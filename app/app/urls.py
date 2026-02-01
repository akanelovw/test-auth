from django.urls import path, include

urlpatterns = [
    path('app/', include('auth.urls')),
    path("app/reports/", include('reports.urls')),
]