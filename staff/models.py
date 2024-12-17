
# -----------------------------PROTOTYPE NUMBER 1------------------------------------

# from django.db import models
# from django.contrib.auth.models import AbstractUser

# # Create your models here.
# class Users(AbstractUser):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=255, unique=True)
#     first_name = models.CharField(null=False, max_length=255)
#     last_name = models.CharField(null=False, max_length=255)
#     image = models.ImageField(upload_to='user-image/',null=True)
#     email = models.CharField(null=False, max_length=64, unique=True)
#     password = models.CharField(max_length = 255, null=False)
#     birth_date = models.DateField(null=True, blank=True)

#     GENDER_CHOICES = [
#         ('M','Male'),
#         ('F','Female'),
#         ('RNS','Rather Not Say')
#     ]
#     gender = models.CharField(max_length=3, choices=GENDER_CHOICES, default='RNS')

#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('employee', 'Employee'),
#         ('user', 'User'),
#     ]
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
#     class Meta:
#         ordering = ['first_name']
        
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']



# -----------------------------PROTOTYPE NUMBER 2------------------------------------


# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db import models

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         extra_fields.setdefault('role', 'user')  # Default role for regular users
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('role', 'admin')  # Set role to admin for superusers

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, **extra_fields)

# class Users(AbstractUser):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=255, unique=True)
#     first_name = models.CharField(null=False, max_length=255)
#     last_name = models.CharField(null=False, max_length=255)
#     image = models.ImageField(upload_to='user-image/', null=True)
#     email = models.CharField(null=False, max_length=64, unique=True)
#     password = models.CharField(max_length=255, null=False)
#     birth_date = models.DateField(null=True, blank=True)

#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('RNS', 'Rather Not Say')
#     ]
#     gender = models.CharField(max_length=3, choices=GENDER_CHOICES, default='RNS')

#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('employee', 'Employee'),
#         ('user', 'User'),
#     ]
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

#     objects = CustomUserManager()  # Use the custom manager

#     class Meta:
#         ordering = ['first_name']

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('role', 'user')  # Default role for regular users
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  
       
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        extra_fields.setdefault('first_name', '')
        extra_fields.setdefault('last_name', '')

        return self.create_user(email, password, **extra_fields)

class Users(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(null=False, max_length=255)
    last_name = models.CharField(null=False, max_length=255)
    image = models.ImageField(upload_to='user-image/', null=True)
    email = models.CharField(null=False, max_length=64, unique=True)
    password = models.CharField(max_length=255, null=False)
    birth_date = models.DateField(null=True, blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('RNS', 'Rather Not Say')
    ]
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES, default='RNS')

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    objects = CustomUserManager()  # Use the custom manager

    class Meta:
        ordering = ['first_name']

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Add first_name and last_name here

