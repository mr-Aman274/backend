from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.files.storage import default_storage
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .authenticate import rideHistory
from .serializer import UserInfoSerializer, loginSerializer, rideInfoSerializer
from .models import UserInfo, rideInfo, vehicleInfo, riderInfo


class userInformation(APIView):  # --> classbased api view
    def get(self, request):  # --> this just list all the users
        userinfo = UserInfo.objects.all()
        serializer = UserInfoSerializer(
            userinfo, many=True
        )  # -> serializes the userinfo for frontend

        return Response(
            {
                "status": 200,
                "payload": serializer.data,
                "message": "Everthing looks good",
            }
        )

    def post(self, request):  # --> create new user
        try:
            data = request.data  # -> extract the data part from the post request
            serializer = UserInfoSerializer(data=data, many=False)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": 200,
                        "payload": serializer.data,
                        "message": "User created sucessfully",
                    }
                )
            return Response({"status": 400, "message": "Something went wrong"})
        except Exception as e:
            print(e)



@api_view(["GET"])
def getOneUserInfo(request, phoneNumber):
    try:
        user = UserInfo.objects.get(phoneNumber=phoneNumber)
        user_id = user.id
        serializer = UserInfoSerializer(user, many=False)
        offered_rides = []
        booked_rides = []
        userVehicleInformation = {}
        img = {}

        if user.isRider:
            try:
                vehicleInforamtion = vehicleInfo.objects.get(user_id=user_id)
                
                userVehicleInformation = {
                    "vehicle_image": vehicleInforamtion.vehicle_image.url,
                    "billbook_page2": vehicleInforamtion.billbook_page2.url,
                    "billbook_page3": vehicleInforamtion.billbook_page9.url
                    }
                img.update(userVehicleInformation)

                offered_rides = rideInfo.objects.filter(user_id=user_id,status='ongoing', rideType="offer")
                print(offered_rides)
                offered_rides_data = rideInfoSerializer(offered_rides[0])
                booked_rides = rideInfo.objects.filter(
                    user_id=user_id, status='ongoing', rideType='book')
                print(booked_rides)
                booked_rides_data = rideInfoSerializer(booked_rides[0])
                return Response({
                "payload": {
                    "img": img,
                    "userInfo": serializer.data,
                    "offeredRides": offered_rides_data.data,
                    "bookedRides": booked_rides_data.data
                },
                "message": "User information obtained sucessfully",
            }, status=200)
            except:
                return Response({
                    "payload":{
                        "userInfo": serializer.data,
                        "offeredRides": offered_rides,
                        "bookedRides": booked_rides
                    },
                     "message": "User information obtained sucessfully",
                }, status=200)

        riderInformation = riderInfo.objects.get(user_id=user_id)
        citizenshipInfos = {
            "citizenship_image_back":riderInformation.citizenship_image_back,
            "citizenship_image_front":riderInformation.citizenship_image_front,
            "id_confirmation_image":riderInformation.id_confirmation_image,
            "user_profile": user.user_profile.url 
        }

        img.update(citizenshipInfos)
        print("-----images-----")
        print(img)
        return Response({
                "payload":{
                    "userInfo": serializer.data,
                    "offeredRides": offered_rides,
                    "bookedRides": booked_rides
                }},status=200)

    except UserInfo.DoesNotExist:
        return Response(
            {
                "status": 404,
                "payload": {},
                "message": "User doesnot exist",
            }
        )

@api_view(['POST'])
def createUser(request):
    try:
        data = request.data  # -!> extract the data part from the post request
        print("-------------------------createUser----------------")
        print(data)
        try:
            user = UserInfo.objects.get(phoneNumber=data['phoneNumber'])
            if user is not None:
                return Response({
                    "message" : "User already exists"
                },status=200)
        except Exception as e:
            new_user = UserInfo.objects.create(
                first_name=data['firstName'],
                last_name=data['lastName'],
                phoneNumber=data['phoneNumber'],
                isRider=True if data['isRider'] == 'true' else False,
                current_address=data['currentAddress'],
                user_profile = request.FILES['image'],
                dob=data['dateOfBirth'].split('T')[0],
            )
            request.session['userId'] = new_user.id
            print("session key", request.session['userId'])
            serializer = UserInfoSerializer(new_user, many=False)
            refresh = RefreshToken.for_user(new_user)
            return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'payload': serializer.data,
                    'verified': True,
                    "message": "User created sucessfully",
                    "rideHistory": {"offered_rides":[], "booked_rides":[], "cancelled_booked_rides": [], "cancelled_offered_rides": [], "completed_book_rides": [], "completed_offered_rides" :[] }
                },status=200
            )
    except Exception as e:
        print(e)
        return Response(
            {"status": 400,
                "message": "`Something` went wrong"
                }
        )


@api_view(["PUT"])  # Put request is to update data
def updateUser(self, request, phoneNumber):  # ---> update the user information
    data = request.data
    try:
        user = UserInfo.objects.get(phoneNumber=phoneNumber)
        for key, value in data.items():
            setattr(user, key, value)
            user.save()
        # UserInfo.objects.filter(id=pk).update(**data) --> Direct method bypass object.save()
        serializer = UserInfoSerializer(user, many=False)
        return Response(
            {
                "status": 201,
                "payload": serializer.data,
                "message": "User info updated sucessfully",
                "payload": {},
            }
        )
    except UserInfo.DoesNotExist:
        return Response(
            {
                "status": 404,
                "message": "User phone number not found",
                "payload": {},
            }
        )


@api_view(["DELETE"])
def deleteUser(request, phoneNumber):  # --> delete the existing user
    try:
        user = UserInfo.objects.get(phoneNumber=phoneNumber)
        user.delete()
        return Response({"status": 200, "message": "User deleted sucessfully", "data": {}})

    except UserInfo.DoesNotExist:
        return Response({
            "status": 404,
            "message": "User phone number not found",
            "payload": {},

        })


class storeRideInfo(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = rideInfoSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": 200,
                        "payload": serializer.data,
                        "message": "Location saved",
                    }
                )
            return Response({
                "message": "serializer not valid"
            })

        except:
            return Response(
                {
                    "status": 400,
                    "error": serializer.errors,
                    "message": "Something went wrong",
                }
            )



def updateStatus(id):
    user = UserInfo.objects.get(id=id)
    user.isRider = True
    user.save()


@api_view(['POST'])
def vehicleInformation(request):
    print("---------------VehicleInfo---------------")
    try:
        data = request.data
        print(data)
        # Get the uploaded image file from the QueryDict
        vehicle_image = request.FILES['vehicleImage']
        billbook_page2 = request.FILES['billBookPage2']
        billbook_page3 = request.FILES['billBookPage3']
        billbook_page9 = request.FILES['billBookPage9']
        license_image = request.FILES['licensePhoto']

        # Create a vehcileInfo instance to save it in the database
        new = vehicleInfo.objects.create(
            user_id=UserInfo.objects.get(id=data["userId"]),
            vehicle_type=data['vehicleType'],
            vehicle_number=data['vehicleRegistrationNumber'],
            vehicle_image=vehicle_image,
            billbook_page2=billbook_page2,
            billbook_page3=billbook_page3,
            billbook_page9=billbook_page9,
            license_image=license_image,
            vehicle_buy_year=data['transportYears'],
            license_number=data['licenseNumber']

        )
        serializer = UserInfoSerializer(new.user_id)
         
        updateStatus(data['userId'])
        return Response({
            "success": "Information added",
            "payload": serializer.data
        }, status=200)

    except Exception as e:
        print(e)
    return Response(
        {
            "error": "something went wrong",
        }, status=400)



@api_view(['POST'])
def updateRideStatus(request):
    rideId = request.data['rideId']
    userId = request.data['userId']
    rideData = rideInfo.objects.get(rideId=rideId)
    userDat = UserInfo.objects.get(id=userId)
    serializedData = UserInfoSerializer(userDat).data
    serializedRiderData = rideInfoSerializer(riderData).data
    print(serializedData)
    print(serializedRiderData)
    rideData.status = "book"
    rideData.user_id = userDat
    rideData.save()
    res = rideHistory(userDat)
    return Response({
        "payload": serializedData,
        "riderData": serializedRiderData,
        "rideHistory": res,
    },status=200)



@api_view(['POST'])
def riderData(request):
    print("----------------riderInfo----------------------")
    data = request.data
    print(request.data)

    # Get the uploaded image files from the QueryDict
    citizenship_image_front = request.FILES['citizenshipImageFront']
    default_storage.save("citizenship_image_front",
                            citizenship_image_front)
    citizenship_image_back = request.FILES['citizenshipImageBack']
    id_confirmation_image = request.FILES['idConfirmationImage']

    new_users_data = riderInfo.objects.create(
        user_id=UserInfo.objects.get(id=data["userId"]),
        citizenship_number=data['citizenshipNumber'],
        citizenship_image_front=citizenship_image_front,
        citizenship_image_back=citizenship_image_back,
        id_confirmation_image = id_confirmation_image
    )
    # # Save the image files to disk using Django's default storage backend
    # default_storage.save('citizenship_front.jpg', citizenship_image_front)
    # default_storage.save('citizenship_back.jpg', citizenship_image_back)
    # default_storage.save('id_confirmation.jpg', id_confirmation_image)

    print(new_users_data.citizenship_image_front.url)
    return Response({
        "message": "Information added"
    }, status=200)


@api_view(['POST'])
def offer_rides(request):
    data = request.data
    print(data)
    rideInfo.objects.create(
        rider = riderInfo.objects.get(user_id=UserInfo.objects.get(id=data['userId'])),
        destination = data['destination'],
        destinationName = data['destinationName'],
        destinationPlaceId = data['destinationPlaceId'],
        origin = data['origin'],
        originPlaceId = data["originPlaceId"],
        originName = data['originName'],
        vehicletype = data['vehicleType'],
        time = data['time'],
        date = data['date'],
    )
    return Response({
        "message": "data saved successfully"
    },status=200)


@api_view(['POST'])
def rideDetail(request):
    data = request.data
    print(data)
    rideId = data['rideId']
    userId = data['userId']
    rideData = rideInfo.objects.get(rideId=rideId)
    riderData = rideData.rider
    print(riderData.id)
    userData = UserInfo.objects.get(id=userId)
    serialized_rideData = rideInfoSerializer(rideData).data
    serialized_userData = UserInfoSerializer(userData).data
    res = {"rideData":serialized_rideData, "userData": serialized_userData}
    info = vehicleInfo.objects.get(id=1)


    return Response({
        "payload" : res,
        "vehicleURL": info.vehicle_image.url,
        "vehicleNumber": info.vehicle_number
    })



@api_view(['GET'])
def getimageUrl(request):
    data = request.data
    # do something to get user data in user
    user = None
    # to get image url do the following
    url = user.test1.url
    return Response({
        "source": url
    })
