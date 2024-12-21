from django.urls import path
from .views import *

urlpatterns = [
    path("user/register/", UserRegisterAPIView.as_view(), name="user_register_view"),
    path("user/login/", UserLoginAPIView.as_view(), name="user_login_view"),

    #For Subject
    path("subject/create/", SubjectCreateAPIView.as_view(), name="subject_create"),
    path("subject/list/", SubjectListAPIView.as_view(), name="subject_list"),
    path("subject/<int:id>/update", SubjectUpdateAPIView.as_view(), name="subject_update"),
    path("subject/<int:id>/delete", SubjectDeleteAPIView.as_view(), name="subject_delete"),
    path("subject/<int:id>/detail", SubjectDetailAPIView.as_view(), name="subject_detail"),

    #For Grade
    path("grade/create/", GradeCreateAPIView.as_view(), name="grade_create"),
    path("grade/list/", GradeListAPIView.as_view(), name="grade_list"),
    path("grade/<int:id>update/", GradeUpdateAPIView.as_view(), name="grade_update"),
    path("grade/<int:id>delete/", GradeDeleteAPIView.as_view(), name="grade_delete"),
    path("grade/<int:id>delete/", GradeDeleteAPIView.as_view(), name="grade_delete"),

    #For Staff
    path("staff/create/", StaffCreateAPIView.as_view(), name="staff_create"),
    path("staff/list/", StaffListAPIView.as_view(), name="staff_list"),
    path("staff/<int:id>update/", StaffUpdateAPIView.as_view(), name="staff_update"),
    path("staff/<int:id>delete/", StaffDeleteAPIView.as_view(), name="staff_delete"),
    path("staff/<int:id>delete/", StaffDetailAPIView.as_view(), name="staff_delete"),

    #For Book
    path("book/create/", BookCreateAPIView.as_view(), name="book_create"),
    path("book/list/", BookListAPIView.as_view(), name="book_list"),
    path("book/<int:id>update/", BookUpdateAPIView.as_view(), name="book_update"),
    path("book/<int:id>delete/", BookDeleteAPIView.as_view(), name="book_delete"),
    path("book/<int:id>delete/", BookDetailAPIView.as_view(), name="book_delete"),

    #For Student
    path("student/create/", StudentCreateAPIView.as_view(), name="student_create"),
    path("student/list/", StudentListAPIView.as_view(), name="student_list"),
    path("student/<int:id>update/", StudentUpdateAPIView.as_view(), name="student_update"),
    path("student/<int:id>delete/", StudentDeleteAPIView.as_view(), name="student_delete"),
    path("student/<int:id>delete/", StudentDetailAPIView.as_view(), name="student_delete"),



]