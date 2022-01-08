
from django.urls import path,include
from .views import face_data,face_data_detail,compare_faces
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('article/', article_list),
    # path('detail/<int:pk>/', article_detail),
    path('face_data/', face_data),
    path('face_data_detail/<int:pk>/', face_data_detail),
    path('compare_faces/', compare_faces),
    # path(r'^upload/$', FileView.as_view(), name='file-upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
