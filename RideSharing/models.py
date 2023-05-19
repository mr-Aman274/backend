from django.db import models
from cloudinary.models import CloudinaryField
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class UserInfo(models.Model):
    # id= models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    phoneNumber = models.CharField(max_length=14, unique=True)
    current_address = models.CharField(max_length=50, blank=True)
    dob = models.CharField(max_length=100, blank=True)
    user_profile = CloudinaryField("user_profile")
    isRider = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phoneNumber"

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name} Phone Number:{self.phoneNumber} and created at {self.created_at}"

class riderInfo(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    # Riders identification
    citizenship_number = models.CharField(max_length=15)
    citizenship_image_back = CloudinaryField(
        "citizenship_image_back", blank=True, null=True)
    citizenship_image_front = CloudinaryField(
        "citizenshipPictures", blank=True, null=True)
    id_confirmation_image = CloudinaryField(
        "idConfirmationPictures", blank=True, null=True)

    timestamp = models.DateTimeField(auto_now=True)


class otp(models.Model):
    phoneNumber = models.CharField(max_length=14)
    otp = models.CharField(max_length=6)


class rideInfo(models.Model):
    STATUS = [('complete', 'complete'), ('cancelled',
                                         'cancelled'), ('ongoing', 'ongoing')]
    RIDETYPE = [('book', 'book'), ('offer', 'offer')]

    rider = models.ForeignKey(riderInfo, on_delete=models.CASCADE, blank=True, null=True)
    time = models.CharField(max_length=10, blank=True, null=True)
    date = models.CharField(max_length=16, blank=True, null=True) 
    rideId = models.AutoField(primary_key=True)
    status = models.CharField(default='ongoing', max_length=10, choices=STATUS)
    rideType = models.CharField(max_length=5, choices=RIDETYPE, default="offer")
    user_id = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)
    destination = models.JSONField(default=dict)
    destinationName = models.CharField(max_length=70, blank=True)
    destinationPlaceId = models.CharField(max_length=50, blank=True)
    origin = models.JSONField(default=dict)
    originName = models.CharField(max_length=70, blank=True)
    originPlaceId = models.CharField(max_length=50, blank=True)
    vehicletype = models.CharField(max_length=10, blank=True)
    timestamp = models.DateTimeField(auto_now=True)



class vehicleInfo(models.Model):
    # vehicle information with billbook

    CAR = "B"
    BIKE = "A"
    VEHICLE_TYPE = [(BIKE, "Bike"), (CAR, "car")]
    rider = models.ForeignKey(riderInfo, on_delete=models.CASCADE, blank=True, null=True)

    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=1, choices=VEHICLE_TYPE)
    vehicle_number = models.CharField(unique=True, max_length=21)
    vehicle_image = CloudinaryField("vehiclePictures", blank=True)
    billbook_page2 = CloudinaryField("billbookPictures")
    billbook_page3 = CloudinaryField("billbookPictures")
    billbook_page9 = CloudinaryField("billbookPictures")
    vehicle_buy_year = models.CharField(max_length=4, blank=True)

    # license information
    license_number = models.IntegerField(unique=True)
    license_image = CloudinaryField("LicensePictures", blank=True)

    timestamp = models.DateTimeField(auto_now=True)


class test1(models.Model):
    image = CloudinaryField('image')
