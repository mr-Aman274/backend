from django.urls import path
from . import views
from .authenticate import loginUser, sendOTP, verifyOTP, checkPhoneNumber, authenticateJWT
from .task import matchUsers



urlpatterns = [
    path('rideStatus', views.updateRideStatus, name="update-ride-status"),
    path('rideDetail', views.rideDetail, name="ride-detail"),
    path('jwt', authenticateJWT, name="authenticate-jwt" ),
    path('checkNumber', checkPhoneNumber, name='check-phone-number'),
    path('createuser/', views.createUser, name='Singn-up'),
    # path('', views.index, name='index'),
    path('searchRides', matchUsers),
    path('login', loginUser.as_view(), name='login-users'),# --> this handles all the get post put and delete request
    path('', views.userInformation.as_view()),
    path('sendotp', sendOTP.as_view(), name = 'Send-otp'),
    path('verifyotp', verifyOTP, name = 'verify-otp'),
    path('users/<str:phoneNumber>', views.getOneUserInfo,
         name='Get-single-user-info'),

    path('update/<str:phoneNumber>',
         views.updateUser, name='Update-user-info'),
    path('delete/<str:phoneNumber>', views.deleteUser, name='delete-user'),
    path('vehicleinformation', views.vehicleInformation, name = 'vehicle-info'),
    path('riderinfo', views.riderData, name = 'rider-info'),
    path('addRide', views.offer_rides, name = 'offer-rides')
]
