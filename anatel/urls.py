from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from . import views

schema_view = get_schema_view(title="API CNL")


urlpatterns = [
    url('^$', schema_view),
    url(r'^upload/$', views.UploadAPIView.as_view(), name='upload_api'),
    url(r'^consult', views.ConsultNumberView.as_view(), name='consult_number_api'),
]
