from django.conf.urls import url
from deals import views


urlpatterns = [
    url('^upload_file/', views.FileUploadView.as_view()),
]
