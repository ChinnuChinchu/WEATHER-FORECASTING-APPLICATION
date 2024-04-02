from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   
   
    path('users/register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('users/login/', UserLoginAPIView.as_view(), name='user-login'),
    path('users/<int:pk>/', UserDetailsAPIView.as_view(), name='user-details'),
    
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    
    # path('posts/', PostCreateAPIView.as_view(), name='post-list-create'),
    # path('posts/<int:pk>/', PostCreateAPIView.as_view(), name='post-detail'),
    
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    
    path('all-posts/', UserPostListAPIView.as_view(), name='user-post-list'),
    
    
    path('posts/search/', PostSearchByLocationAPIView.as_view(), name='post-search-by-location'),
    path('posts/<int:post_id>/like/', PostLikeAPIView.as_view(), name='post-like'),
    
    path('posts/<int:post_id>/comment/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('posts/<int:post_id>/comment/<int:comment_id>/', CommentCreateAPIView.as_view(), name='comment-detail'),
    
    path('posts/<int:post_id>/comments/', PostCommentsAPIView.as_view(), name='post_comments'),
    
    path('superuser-login/', SuperuserLoginView.as_view(), name='superuser-login'),
    
    path('emergencies/', EmergencyAPIView.as_view(), name='emergency-list'),
    path('emergencies/<int:pk>/', EmergencyDetailAPIView.as_view(), name='emergency-detail'),
    
    path('get-emergencies-all/', EmergencyDetailAPIView.as_view(), name='emergency-list'),
    
    path('user-badges/', UserBadgesAPIView.as_view(), name='user-badges'),
]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)