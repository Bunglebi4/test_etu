from django.urls import path
from converter.views import to_xml, from_xml

urlpatterns = [
    path('to_xml/', to_xml, name='to_xml'),
    path('from_xml/', from_xml, name='from_xml'),
]
