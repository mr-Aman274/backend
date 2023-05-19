from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.conf import settings
from django.db.models import Q

from twilio.rest import Client
from random import randint
import jwt

from .serializer import UserInfoSerializer, loginSerializer, rideInfoSerializer
from .models import UserInfo, otp, rideInfo, riderInfo



def rideHistory(user):
    try:
        if user.isRider:
            print(user.id)
            rider = riderInfo.objects.get(user_id=user)

            offered_rides = rideInfo.objects.filter(rideType="offer").filter(Q(rider=rider,status='ongoing')| Q(status='book'))

            cancelled_offered_rides = rideInfo.objects.filter(rider=rider, status='cancelled',rideType="offer")

            completed_offered_rides = rideInfo.objects.filter(rider=rider, status='complete',rideType="offer")

            completed_book_rides = rideInfo.objects.filter(user_id=user, status='complete',rideType="book")

            booked_rides = rideInfo.objects.filter(user_id=user, status='book', rideType='offer')
            cancelled_booked_rides = rideInfo.objects.filter(user_id=user, status='cancelled',rideType="book")
            s1 = rideInfoSerializer(offered_rides, many=True).data
            s4 = rideInfoSerializer(cancelled_offered_rides, many=True).data
            s6 = rideInfoSerializer(completed_offered_rides, many=True).data

            s5 = rideInfoSerializer(completed_book_rides, many=True).data
            s3 = rideInfoSerializer(cancelled_booked_rides, many=True).data
            s2 = rideInfoSerializer(booked_rides, many=True).data
            res = {"offered_rides":s1, "booked_rides":s2, "cancelled_booked_rides": s3, "cancelled_offered_rides": s4, "completed_book_rides": s5, "completed_offered_rides" : s6}
            return res
        else:
            booked_rides = rideInfo.objects.filter(user_id=user, status='book', rideType='offer')
            cancelled_booked_rides = rideInfo.objects.filter(user_id=user, status='cancelled',rideType="book")
            completed_book_rides = rideInfo.objects.filter(user_id=user, status='complete',rideType="book")
            s5 = rideInfoSerializer(completed_book_rides, many=True).data
            s3 = rideInfoSerializer(cancelled_booked_rides, many=True).data
            s2 = rideInfoSerializer(booked_rides, many=True).data
            res = { "booked_rides":s2, "cancelled_booked_rides": s3, "completed_book_rides": s5}
            return res
    except Exception as e:
        print(e)
        return {}



@api_view(['POST'])
def checkPhoneNumber(request):
    try:
        data = request.data
        phoneNumber = data['phoneNumber']
        UserInfo.objects.get(phoneNumber=phoneNumber)
        return Response({
            "response": True,

        },status=200)
    except UserInfo.DoesNotExist:
        return Response({
            "error": "User doesn't exist!!"
        },status=404)


@api_view(['POST'])
def authenticateJWT(request):
    try:
        data = request.data
        print(data)
        jwtoken = data['token']

        secret_key = settings.SIMPLE_JWT['SIGNING_KEY']

        decoded_data = jwt.decode(jwtoken, secret_key, algorithms=['HS256'])
        print(decoded_data)
        user = UserInfo.objects.get(id=decoded_data['user_id'])
        serializer = UserInfoSerializer(user)
        res = rideHistory(user)
        print(res)
        return Response({
            "payload": serializer.data,
            "rideHistory": res
        },status=200)
    except:
        pass

        return Response({
            "message": "NOT FOUND"
        },status=404)



class loginUser(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = loginSerializer(data=data)
            if serializer.is_valid():
                phoneNumber = serializer.validated_data['phoneNumber']
                try:
                    user = UserInfo.objects.get(phoneNumber=phoneNumber)
                    print("--------------login-------------")
                except UserInfo.DoesNotExist:
                    return Response({
                        "status": 404,
                        "message": "Phone number not found",
                        "paylaod": {},
                    })
                serializer = UserInfoSerializer(user)
                refresh = RefreshToken.for_user(user)
                res = rideHistory(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'payload': serializer.data,
                    'rideHistory': res
                })
        except Exception as e:
            print(e)
            return Response({
                "message": "Internal server error",
                "payload": {}
            }, status=500)


class sendOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data['phoneNumber'])
            phoneNumber = "+977" + data['phoneNumber']
            otp_value = randint(100000, 999999)
            print("---------otp--------")
            print(otp_value)

            mew = otp.objects.create(
                phoneNumber=phoneNumber,
                otp=otp_value
            )
            print("mew.phonenumber",mew.phoneNumber)

            client = Client(settings.TWILIO_ACCOUNT_SID,
                            settings.TWILIO_AUTH_TOKEN)

            client.messages.create(
                body="Your OTP for ride sharing app is " + str(otp_value),
                from_=settings.TWILIO_FROM_NUMBER,
                to=phoneNumber
            )
            return Response({
                "message": " OTP sent",
                "payload": {},
                "response": True,
            }, status=200)

        except Exception as e:
            print(e)
            return Response({
                "message": "something went wrong",
                "payload": {},
                "response": False,
            })


@api_view(['POST'])
def verifyOTP(request):
    print("-----Verify OTP-----")
    try:
        data = request.data
        print("--------otp from forntend------------")
        phoneNumber = '+977' + data['phoneNumber']  # -----+977
        print(phoneNumber)
        otp_value = data['otp']

        print(otp_value)

        user = otp.objects.filter(
            phoneNumber=phoneNumber, otp=otp_value).last()
        if user is None:
            print("not verified")
            return Response({
                "message": "OTP didnot matched",
                "payload": {},
                "response": False
            }, status=200)

        print("verified")
        return Response({
            "message": "OTP verified",
            "paylaod": {},
            "response": True,
        }, status=200)

    except Exception as e:
        print(e)
        return Response({
            "message": "Something went wrong",
            "payload": {},
        }, status=400)
