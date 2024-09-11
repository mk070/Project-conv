from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.ProjectUploadView.as_view(), name='upload'),
    path('convert/', views.ProjectConvertView.as_view(), name='convert'),
    path('download/', views.ProjectDownloadView.as_view(), name='download'),
]
