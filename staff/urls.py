from django.urls import path, include

from staff import views

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view()),
    path('user/', views.UserView.as_view()),
    path('users/', views.UsersView.as_view()),
    path('user-count/',views.UsersCountView.as_view()),
    path('update_profile/<int:pk>/', views.UpdateProfileView.as_view(), name='auth_update_profile'),
]