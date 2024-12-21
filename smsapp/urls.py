# smsapp/urls.py
from django.urls import path
from .views import *
app_name = 'smsapp'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    #
    path('staff/list', StaffListView.as_view(), name='staff_list'),
    path('staff/create', StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:id>update', StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:id>delete', StaffDeleteView.as_view(), name='staff_delete'),
    path('staff/<int:id>detail', StaffDetailView.as_view(), name='staff_detail'),

    path('grade/create', GradeCreateView.as_view(), name='grade_create'),
    path('grade/list', GradeListView.as_view(), name='grade_list'),

    path('subject/create', SubjectCreateView.as_view(), name='subject_create'),
    path('subject/list', SubjectListView.as_view(), name='subject_list'),
    path('subject/<int:id>/update/', SubjectUpdateView.as_view(), name='subject_update'),
    path('subject/<int:id>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),


    path('student/create', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:id>/update', StudentUpdateView.as_view(), name='student_update'),
    path('student/<int:id>/delete', StudentDeleteView.as_view(), name='student_delete'),
    path('student/list', StudentListView.as_view(), name='student_list'),
    path('student/<int:id>detail', StudentDetailView.as_view(), name='student_detail'),

    path('books/create', BooksCreateView.as_view(), name='books_create'),
    path('books/list', BooksListView.as_view(), name='books_list'),
    path('books/<int:id>/delete', BooksDeleteView.as_view(), name='books_delete'),
    path('books/<int:id>/update', BooksUpdateView.as_view(), name='books_update'),
    path('books/<int:id>/detail', BooksDetailView.as_view(), name='books_detail'),



    path('attendance/create', AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendance/list', AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/<int:id>update', AttendanceUpdateView.as_view(), name='attendance_update'),
    path('attendance/<int:id>delete', AttendanceDeleteView.as_view(), name='attendance_delete'),


    path('exam/create', ExamCreateView.as_view(), name='exam_create'),
    path('exam/list', ExamListView.as_view(), name='exam_list'),
    path('exam/<int:id>update', ExamUpdateView.as_view(), name='exam_update'),
    path('exam/<int:id>delete', ExamDeleteView.as_view(), name='exam_delete'),
    path('exam/<int:id>detail', ExamDetailView.as_view(), name='exam_detail'),



    path('result/create', ResultCreateView.as_view(), name='result_create'),
    path('result/list', ResultListView.as_view(), name='result_list'),
    path('result/<int:id>update', ResultUpdateView.as_view(), name='result_update'),
    path('result/<int:id>delete', ResultDeleteView.as_view(), name='result_delete'),
    path('result/<int:id>detail', ResultDetailView.as_view(), name='result_detail'),

        #For login/logout/
    path('login/', CustomerLoginView.as_view(), name='customer_login'),
    path('logout/', CustomerLogoutView.as_view(), name='customer_logout'),
    path('signup/', CustomerRegisterView.as_view(), name='customer_registration'),
    
    path('search/', SearchView.as_view(), name='search_product'),


]
