from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   
   
    path('users/register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('users/login/', UserLoginAPIView.as_view(), name='user-login'),
    path('users/<int:pk>/', UserDetailsAPIView.as_view(), name='user-details'),
    
    path('posts/', PostCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostCreateAPIView.as_view(), name='post-detail'),
    path('posts/search/', PostSearchByLocationAPIView.as_view(), name='post-search-by-location'),
    path('posts/<int:post_id>/like/', PostLikeAPIView.as_view(), name='post-like'),
    path('posts/<int:post_id>/comment/', CommentCreateAPIView.as_view(), name='comment-create'),
    
    path('superuser-login/', SuperuserLoginView.as_view(), name='superuser-login'),
    
    path('emergencies/', EmergencyAPIView.as_view(), name='emergency-list'),
    path('emergencies/<int:pk>/', EmergencyDetailAPIView.as_view(), name='emergency-detail'),
]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)