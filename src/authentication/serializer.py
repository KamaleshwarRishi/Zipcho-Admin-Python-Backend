from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, profile

class UserSerializer(serializers.ModelSerializer):
    class Meta : 
        model = User 
        fields = ['id', 'email']

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta : 
        model = User
        fields = ['id', 'email', 'token']
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class profilePicSerializer(serializers.ModelSerializer):
    class Meta: 
        model  = profile
        fields = ['profileImage']
