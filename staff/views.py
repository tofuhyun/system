from .serializers import UserSerializer, UsersSerializer, UpdateUserSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .models import Users
#from rest_framework import generics
#from .permissions import IsAdminUser, IsEmployeeUser
import logging
from permissions import IsAdminUser
from rest_framework.generics import UpdateAPIView
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView



# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logging.info(refresh_token)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logging.error(f"Logout error: {str(e)}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = request.user
        serializer = UserSerializer(data, many=False)
        return Response(serializer.data)
    
class UsersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        data = Users.objects.all()
        serializer = UsersSerializer(data, many=True, context={'request': self.request})
        return Response(serializer.data)
    
class UsersCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_count = Users.objects.count()
        return Response({
            'user_count': user_count
        }, status=200)    
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




# CODE MO TO DREI 


# class UpdateProfileView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = UpdateUserSerializer

#     def put(self, request, *args, **kwargs):
#         data = request.data
#         pk = kwargs.get('pk')
#         try:
#             instance = Users.objects.get(id=pk)  # Use data['id'] to access the id
#         except Users.DoesNotExist:
#             return Response({'error': 'User  not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = self.get_serializer(instance, data=data, partial=True)  # Pass instance and data to serializer

#         if serializer.is_valid():
#             serializer.save()  # Save the updated instance
#             return Response(serializer.data, status=status.HTTP_200_OK)  # Return updated data
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors



# CODE NI HENRY TO


class UpdateProfileView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UpdateUserSerializer

    def put(self, request, *args, **kwargs):
        data = request.data
        pk = kwargs.get('pk')

      
        logging.info(f"Request Data: {data}")
        
        try:
            instance = Users.objects.get(id=pk)  
        except Users.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        logging.info(f"User Instance: {instance}")

        serializer = self.get_serializer(instance, data=data, partial=True)  # partial=True for partial update

        if serializer.is_valid():
            serializer.save()  
            logging.info(f"Updated User Data: {serializer.data}")  
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        logging.error(f"Serializer Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Ensure this import is at the top of your file
# GOOGLE_REDIRECT_URL = "http://localhost:8000/accounts/google/login/callback/" 

# class GoogleLoginView(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = GOOGLE_REDIRECT_URL
#     client_class = OAuth2Client
