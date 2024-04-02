from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



        
class SuperuserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    

class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = '__all__'


############## User #####################

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','first_name','last_name','username','email']
        
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    
################# Post ############


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id', 'user','user_username','post', 'text', 'created_at')
    
    def get_user_username(self, obj):
        return obj.user.username
        
  

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'image', 'description', 'user','created_at', 'location', 'likes', 'comments','reports_count')
        read_only_fields = ('likes', 'comments','user')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_username'] = instance.user.username
        return representation
        
   


    
