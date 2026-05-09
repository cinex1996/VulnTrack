from django.urls import path
from vulnerabilities import views

urlpatterns = [
    path('',views.index,name='index'),
    path('detail/<int:id>/',views.vulnerability_detail,name='vulnerability_detail'),
    path('create/',views.create_vulnerability,name='create_vulnerability'),
    path('edit/<int:id>/',views.update_vulnerability,name='update_vulnerability'),
    path('delete/<int:id>/',views.delete_vulnerability,name='delete_vulnerability'),
]
