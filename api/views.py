from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
import base64
from django.conf import settings
from PIL import Image, UnidentifiedImageError

from PIL import Image
from io import BytesIO
from django.shortcuts import get_object_or_404

import os
import random

from .serializers import *
from smsapp.models import *


# Custom permission for admin or read-only access
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff


# User registration API
class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers


# User login API
class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class GradeListAPIView(APIView):
    """
    API View to list all Grades
    """
    def get(self, request):
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class GradeCreateAPIView(APIView):
    """
    API View to create a new Grade
    """
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors, 'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)


class GradeUpdateAPIView(APIView):
    """
    API View to update an existing Grade
    """
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, id):
        grade = get_object_or_404(Grade, id=id)
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors, 'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)


class GradeDeleteAPIView(APIView):
    """
    API View to delete a Grade
    """
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, id):
        grade = get_object_or_404(Grade, id=id)
        grade.delete()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class GradeDetailAPIView(APIView):
    """
    API View to retrieve details of a specific Grade
    """
    def get(self, request, id):
        grade = get_object_or_404(Grade, id=id)
        serializer = GradeSerializer(grade)
        return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)
    
#Subject
class SubjectListAPIView(APIView):
    """
    API View to list all Subjects
    """
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class SubjectCreateAPIView(APIView):
    """
    API View to create a new Subject
    """
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors, 'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)


class SubjectUpdateAPIView(APIView):
    """
    API View to update an existing Subject
    """
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, id):
        subject = get_object_or_404(Subject, id=id)
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors, 'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)


class SubjectDeleteAPIView(APIView):
    """
    API View to delete a Subject
    """
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, id):
        subject = get_object_or_404(Subject, id=id)
        subject.delete()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class SubjectDetailAPIView(APIView):
    """
    API View to retrieve details of a specific Subject
    """
    def get(self, request, id):
        subject = get_object_or_404(Subject, id=id)
        serializer = SubjectSerializer(subject)
        return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)


#For Staff
class StaffCreateAPIView(APIView):
    def base64_to_image(self, base64_string, file_path):
        try:
            # Ensure the directory exists
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            # Handle base64 prefix
            if base64_string.startswith('data:image'):
                base64_string = base64_string.split(',')[1]

            # Decode base64 string
            image_bytes = base64.b64decode(base64_string)
            image_buffer = BytesIO(image_bytes)
            image = Image.open(image_buffer)
            image.verify()  # Validate the image
            image = Image.open(image_buffer)  # Re-open after verification

            # Generate unique file name
            random_integer = random.randint(100, 999)
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
            image_name = f"staff-{formatted_date}-{random_integer}.jpg"

            image_path = os.path.join(file_path, image_name)

            # Save the image
            image.save(image_path, "JPEG")
            return image_path
        except UnidentifiedImageError:
            print("Error: The provided base64 string is not a valid image.")
            return None
        except Exception as e:
            print(f"Error in image processing: {e}")
            return None

    def post(self, request):
        file_path = os.path.join(settings.MEDIA_ROOT, "staff/")
        base64_image = request.data.get("profile_picture")
        print(base64_image,'mmm ')

        # Validate base64 string
        if not base64_image or not self.is_valid_base64(base64_image):
            return Response({"message": "Invalid base64 image data."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert the base64 image string to an image and save it
        photo_path = self.base64_to_image(base64_image, file_path)

        if not photo_path:
            return Response({"message": "Image processing failed."}, status=status.HTTP_400_BAD_REQUEST)

        # Pass the modified data to the serializer
        data = request.data.copy()
        data["profile_picture"] = photo_path
        serializer = StaffSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_valid_base64(self, base64_string):
        try:
            base64.b64decode(base64_string, validate=True)
            return True
        except base64.binascii.Error:
            return False


class StaffListAPIView(APIView):
    """
    API View to list all Subjects
    """
    def get(self, request):
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

class StaffUpdateAPIView(APIView):
    """
    API View to update an existing Subject
    """
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, id):
        subject = get_object_or_404(Subject, id=id)
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors, 'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)


class StaffDeleteAPIView(APIView):
    """
    API View to delete a Subject
    """
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, id):
        subject = get_object_or_404(Subject, id=id)
        subject.delete()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class StaffDetailAPIView(APIView):
    """
    API View to retrieve details of a specific Subject
    """
    def get(self, request, id):
        staff = get_object_or_404(Subject, id=id)
        serializer = StaffSerializer(staff)
        return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)
    

#Book
class BookCreateAPIView(APIView):
    """
    API View to create a new Grade
    """
    permission_classes = [IsAdminOrReadOnly]

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors, 'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)


class BookListAPIView(APIView):
    """
    API View to list all Subjects
    """
    def get(self, request):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class BookUpdateAPIView(APIView):
    """
    API View to update an existing Subject
    """
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, id):
        book = get_object_or_404(Subject, id=id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors, 'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)


class BookDeleteAPIView(APIView):
    """
    API View to delete a Subject
    """
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, id):
        book = get_object_or_404(Book, id=id)
        book.delete()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class BookDetailAPIView(APIView):
    """
    API View to retrieve details of a specific Subject
    """
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        serializer = StaffSerializer(book)
        return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)
    

#For Student
class StudentCreateAPIView(APIView):
    # permission_classes = [IsAdminOrReadOnly]

    def base64_to_image(self, base64_string, file_path):
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            image_bytes = base64.b64decode(base64_string)
            image_buffer = BytesIO(image_bytes)
            image = Image.open(image_buffer)

            random_integer = random.randint(100, 999)
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
            image_name = f"article-{formatted_date}-{random_integer}.jpg"

            image_path = os.path.join(file_path, image_name)
            image.save(image_path, "JPEG")

            return image_path
        except Exception as e:
            print(f"Error in image processing: {e}")
            return None

    def post(self, request):
        file_path = "/app/media/student/"
        photo = self.base64_to_image(request.data.get('image'), file_path)

        if not photo:
            return Response({"message": "Image processing failed."}, status=status.HTTP_400_BAD_REQUEST)

        image_data = request.data.copy()
        image_data['image'] = photo

        serializer = StudentSerializer(data=image_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentListAPIView(APIView):
    """
    API View to list all Subjects
    """
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class StudentUpdateAPIView(APIView):
    """
    API View to update an existing Subject
    """
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, id):
        student = get_object_or_404(Subject, id=id)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors, 'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)


class StudentDeleteAPIView(APIView):
    """
    API View to delete a Subject
    """
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, id):
        student = get_object_or_404(Student, id=id)
        student.delete()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class StudentDetailAPIView(APIView):
    """
    API View to retrieve details of a specific Subject
    """
    def get(self, request, id):
        student = get_object_or_404(Book, id=id)
        serializer = StudentSerializer(student)
        return Response({'data': serializer.data, 'status': 'success'}, status=status.HTTP_200_OK)
    
