from smsapp.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','date_joined']



class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Create the user with the hashed password
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user

    def to_representation(self, instance):
        # Get the original serialized data
        data = super().to_representation(instance)
        
        # Add the hashed password to the response
        # The password will be hashed by Django automatically
        data['password'] = instance.password
        
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        
        # Return the user object if credentials are correct
        data["user"] = user
        return data

#For Grade
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ["name","description"]

#For Subject
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id","name","grade","description"]

#For Staff
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["name","role","subject","phone","email","address","date_of_birth","hire_date","profile_picture","is_active","qualifications"]

#For Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["grade","subject","title","author","publication_date","publisher","page_count","language","available_copies",]

#For Student
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["name","roll_number","grade","date_of_birth","gender","email","phone","address","admission_date","profile_picture","parent_name","parent_name","parent_contact","is_active"]


#For 
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["name","roll_number","grade","date_of_birth","gender","email","phone","address","admission_date","profile_picture","parent_name","parent_name","parent_contact","is_active"]
