from django.conf.urls import include
from django.urls import path
from .v1.generatePDF.router import urlpatterns as generate_pdf_url
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('v1/auth/api-token-auth', obtain_auth_token),
    path('v1/generatePDF/', include(generate_pdf_url)),
]