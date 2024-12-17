from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.files.storage import default_storage
from .models import Users
import logging

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'gender', 
            'birth_date',
            'password',
            'role'
            ]
        extra_kwargs = {
            'password': {'write_only':True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom response data
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email
        }

        return data
    
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'first_name',
            'image',
            'last_name',
            'email',
            'birth_date',
            'gender',
            'role'
        ]


# OLD CODE MO TO KZANDREI SA BABA YUNG KAPALIT NA TEST (DI RIN GUMAGANA HAHA)


# class UpdateUserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True)

#     class Meta:
#         model = Users
#         fields = ('username', 'first_name', 'last_name','image', 'email', 'birth_date', 'gender','role')
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': True},
#         }

#     def update(self, instance, validated_data):
#     # Handle the image upload
#         image = validated_data.pop('image', None)

#         # If there is a new image, delete the old one
#         if image:
#             # Check if the instance has an existing image and delete it
#             if instance.image:
#                 # Remove the old image file
#                 if default_storage.exists(instance.image.name):
#                     default_storage.delete(instance.image.name)

#             # Set the new image
#             instance.image = image

#         for attr in ['username', 'first_name', 'last_name', 'birth_date', 'gender', 'role']:
#             if attr in validated_data:
#                 setattr(instance, attr, validated_data[attr])

#         instance.save()
#         return instance






class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'image', 'email', 'birth_date', 'gender', 'role')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def update(self, instance, validated_data):

        image = validated_data.pop('image', None)


        logging.info(f"Updating user {instance.id} with data: {validated_data}")

       
        if image:
        
            if instance.image:
    
                if default_storage.exists(instance.image.name):
                    default_storage.delete(instance.image.name)
                    logging.info(f"Deleted old image: {instance.image.name}")

            instance.image = image
            logging.info(f"New image set: {image.name}")
 
        for attr in ['username', 'first_name', 'last_name', 'birth_date', 'gender', 'role']:
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])

        logging.info(f"Updated user {instance.id}: {instance}")
       
        instance.save()
        return instance

