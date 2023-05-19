from rest_framework import serializers
from .models import UserInfo, rideInfo, riderInfo, vehicleInfo


class UserInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserInfo 
		fields = '__all__'


class loginSerializer(serializers.Serializer):
	phoneNumber = serializers.CharField()


class rideInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = rideInfo
		fields = '__all__'


class riderInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = riderInfo
		fields = '__all__'


class vehicleInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = vehicleInfo
		fields = '__all__'
