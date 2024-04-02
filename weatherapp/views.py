from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.http import Http404 
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
import random
import string


class SuperuserLoginView(APIView):
    # permission_classes = [IsAdminUser] 

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        serializer = SuperuserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            # Include superuser details in the response
            superuser_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                
            }

            # Using Django's Token model to generate a normal token
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'superuser': superuser_data, 'message': "Logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials or user is not a superuser'}, status=status.HTTP_401_UNAUTHORIZED)


        
        
        
################### EMERGENCY ####################
class EmergencyAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        emergencies = Emergency.objects.all()
        serializer = EmergencySerializer(emergencies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmergencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmergencyDetailAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get_object(self, pk):
        try:
            return Emergency.objects.get(pk=pk)
        except Emergency.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        emergency = self.get_object(pk)
        serializer = EmergencySerializer(emergency)
        return Response(serializer.data)

    def put(self, request, pk):
        emergency = self.get_object(pk)
        serializer = EmergencySerializer(emergency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        emergency = self.get_object(pk)
        emergency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

######################## EMERGENCY GET ALL ####################

class EmergencyDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        emergencies = Emergency.objects.all()
        serializer = EmergencySerializer(emergencies, many=True)
        return Response(serializer.data)

################### USER ####################

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to register
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            serialized_user=UserSerializer(user)
            return Response(serialized_user.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=400)

class UserDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserEditSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserEditSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User details updated successfully'})
        else:
            return Response(serializer.errors, status=400)
        
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
        
        
class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                serialized_user = UserSerializer(user)
                return Response({
                    'user': serialized_user.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class ForgotPasswordView(APIView):
    def post(self, request):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)

            # Generate a new password
            new_password = generate_random_otp()

            # Update the user's password in the database
            user.set_password(new_password)
            user.save()

            # Send the new password to the user's email
            response = self.send_new_password_to_user_email(user, new_password)
            
            return response
        except ObjectDoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Helper function to send the new password to the user's email
    def send_new_password_to_user_email(self, user, new_password):
        subject = 'New Password'
        message = f'Your new password is: {new_password}'
        from_email = 'chinchuofficialweb@gmail.com'  # Update with your email
        recipient_list = [user.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({'msg': 'New password sent successfully'})
        except BadHeaderError:
            return Response({'msg': 'Invalid header found in the email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'msg': f'Error sending email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_random_otp():
    return ''.join(random.choices(string.digits, k=6))



#reset password

class ResetPasswordView(APIView):
    def post(self, request):
        username = request.data.get('username')
        new_password = request.data.get('new_password')

        if not username or not new_password:
            return Response({'msg': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)

            # Reset password using set_password method
            user.set_password(new_password)
            user.save()

            return Response({'msg': 'Password reset successfully'})
        except ObjectDoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

        
        
 ########################## Post creation ############################       


class PostListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, user=request.user,status=True)
            
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
######################## GET ALL THE USERS POSTS ####################


class UserPostListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve all posts for all users
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        data=serializer.data
        
        for i,post_data in enumerate(data):
            username=posts[i].user.username
            data[i]['username']=username
        return Response(data, status=status.HTTP_200_OK)
    
####################### POST LIKE AND COMMENTS #################

class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        post.save()
        
        # Get the count of likes for the post
        likes_count = post.likes.count()
        
        serializer = PostSerializer(post)
        
        # Serialize the user data
        user_data = {
            'id': user.id,
            'username': user.username,
            
        }
        # Prepare the response data
        response_data = {
            'post': serializer.data,
            'liked_user': user_data,
            'liked': liked,
            'likes_count':likes_count
        }
        return Response(response_data)
    
    

class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def get(self,request,post_id,comment_id):
        try:
            comment=Comment.objects.get(id=comment_id,post_id=post_id)
        except Comment.DoestNotExist:
            return Response({'error':'Comment not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            comment_instance = serializer.instance
            comment_data = CommentSerializer(comment_instance).data
            post_data = PostSerializer(post).data
            response_data = {
                'post': post_data,
                'user': request.user.username,
                'comment': comment_data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, post_id=post_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, post_id=post_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
##################### COMMENT ALL #########################

class PostCommentsAPIView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            comments = post.comments.all()  # Get all comments related to the post
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


    
######################### Post search ###############
class PostSearchByLocationAPIView(APIView):
    def get(self, request):
        location = request.query_params.get('location', None)
        if location:
            posts = Post.objects.filter(location__icontains=location)
            serializer = PostSerializer(posts, many=True)
            posts_count = posts.count()  # Count of posts
            response_data = {
                'posts': serializer.data,  # Serialized posts
                'posts_count': posts_count  # Count of posts
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Location parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        
################ Badges ############


# class UserBadgesAPIView(APIView):
#     def get(self, request):
#         users = User.objects.all()
#         badges = []

#         for user in users:
#             post_count = Post.objects.filter(user=user).count()
#             badge, badge_image = self.assign_badge(post_count)
#             badges.append({'user': user.username, 'badge': badge, 'badge_image': badge_image})

#         return Response({'badges': badges}, status=status.HTTP_200_OK)

#     def assign_badge(self, post_count):
#         if post_count >= 10:
#             return "Gold", "/static/star_gold.jpg"  # URL of Gold badge image
#         elif post_count >= 5:
#             return "Silver", "/static/star_silver.jpg"  # URL of Silver badge image
#         elif post_count >= 1:
#             return "Bronze", "/static/star_bronze.jpg"  # URL of Bronze badge image
#         else:
#             return "No Badge", ""  # No badge image needed for No Badge

class UserBadgesAPIView(APIView):
    def get(self, request):
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            post_count = Post.objects.filter(user=user).count()
            badge, badge_image = self.assign_badge(post_count)
            response_data = {'user': user.username, 'badge': badge, 'badge_image': badge_image}
            return Response(response_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def assign_badge(self, post_count):
        if post_count >= 10:
            return "Gold", "/static/star_gold.jpg"  # URL of Gold badge image
        elif post_count >= 5:
            return "Silver", "/static/star_silver.jpg"  # URL of Silver badge image
        elif post_count >= 1:
            return "Bronze", "/static/star_bronze.jpg"  # URL of Bronze badge image
        else:
            return "No Badge", ""  # No badge image needed for No Badge