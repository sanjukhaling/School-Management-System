from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Grade, Staff, Subject, Book, Student, Attendance, Exam, Result

admin.site.register(Grade)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Exam)
admin.site.register(Result)
