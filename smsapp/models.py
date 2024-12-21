from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This makes DateTimeModel an abstract base class


# Grade Model
class Grade(DateTimeModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Subject Model
class Subject(DateTimeModel):
    name = models.CharField(max_length=100, unique=True)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Staff Model (Updated to Include Teaching Role)
class Staff(DateTimeModel):
    ROLE_CHOICES = [
        ('Teacher', 'Teacher'),
        ('Librarian', 'Librarian'),
        ('Music Teacher', 'Music Teacher'),
        ('Nurse', 'Nurse'),
        ('Security Guard', 'Security Guard'),
        ('Janitor', 'Janitor'),
        ('Physical Education Teacher', 'Physical Education Teacher'),
        ('Finance Officer', 'Finance Officer'),
        ('IT Administrator', 'IT Administrator'),
        ('Administrative Officer', 'Administrative Officer'),
        ('Principal', 'Principal'),
        ('Vice Principal', 'Vice Principal'),
        ('Transport Coordinator', 'Transport Coordinator'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Teacher')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Changed to CharField
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    hire_date = models.DateField()
    profile_picture = models.ImageField(upload_to='staff/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"



# Book Model
from django.db import models

class Book(models.Model):  # Assuming `DateTimeModel` is not providing necessary functionality.
    grade = models.ForeignKey(
        'Grade', 
        on_delete=models.CASCADE, 
        related_name='books', 
        blank=True, 
        null=True
    )
    subject = models.ForeignKey(
        'Subject', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    title = models.CharField(
        max_length=200, 
        blank=False,  # Ensures the title is required.
        null=False
    )
    author = models.CharField(
        max_length=100, 
        blank=False,  # Ensures the author is required.
        null=False
    )
    isbn = models.CharField(
        max_length=13, 
        blank=True,  # ISBN should be required.
        null=True
    )
    publication_date = models.DateField(
        blank=True,  # Allows blank date for drafts or unknown publication dates.
        null=True
    )
    publisher = models.CharField(
        max_length=200, 
        blank=True, 
        null=True
    )
    page_count = models.PositiveIntegerField(  # Enforce non-negative values for page count.
        blank=True, 
        null=True
    )
    language = models.CharField(
        max_length=50, 
        default='English', 
        blank=True, 
        null=True
    )
    available_copies = models.PositiveIntegerField(  # Use PositiveIntegerField for non-negative values.
        default=0, 
        blank=True, 
        null=False
    )

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title if self.title else "Unnamed Book"



# Student Model
class Student(DateTimeModel):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=10, unique=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='students')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Changed to CharField
    address = models.CharField(max_length=255, blank=True, null=True)
    admission_date = models.DateField()
    profile_picture = models.ImageField(upload_to='students/', blank=True, null=True)
    parent_name = models.CharField(max_length=100, blank=True, null=True)
    parent_contact = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Attendance Model (Updated to Use Staff)

class Attendance(models.Model):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Staff', 'Staff'),
    ]

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='attendance', null=True, blank=True)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='attendance', null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    check_in_time = models.TimeField(null=True, blank=True)  # Use TimeField for time-only values
    check_out_time = models.TimeField(null=True, blank=True)

    def clean(self):
        # Ensure either student or staff is selected based on the role
        if self.role == 'Student' and not self.student:
            raise ValidationError("Student must be selected for role 'Student'.")
        if self.role == 'Staff' and not self.staff:
            raise ValidationError("Staff must be selected for role 'Staff'.")
        if self.role == 'Student' and self.staff:
            raise ValidationError("Staff should not be selected when role is 'Student'.")
        if self.role == 'Staff' and self.student:
            raise ValidationError("Student should not be selected when role is 'Staff'.")

    def __str__(self):
        return f"{self.student or self.staff} - {self.date} - {self.status}"


# Exam Model
class Exam(DateTimeModel):
    EXAM_TYPE_CHOICES = [
        ('Mid-Term', 'Mid-Term'),
        ('Final-Term', 'Final-Term'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='exams')
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.name} - {self.exam_type} - {self.date}"



# Result Model

class Result(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('C+', 'C+'),
        ('C', 'C'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, null=True, blank=True)
    date = models.DateField()

    score = models.FloatField()
    total_marks = models.FloatField()
    percentage = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Example of a timestamp field


    def clean(self):
        # Validate score is not greater than total marks
        if self.score > self.total_marks:
            raise ValidationError("Score cannot be greater than total marks.")

    def save(self, *args, **kwargs):
        if self.total_marks > 0:
            self.percentage = (self.score / self.total_marks) * 100
            if self.percentage >= 90:
                self.grade = 'A+'
            elif self.percentage >= 80:
                self.grade = 'A'
            elif self.percentage >= 70:
                self.grade = 'B+'
            elif self.percentage >= 60:
                self.grade = 'B'
            elif self.percentage >= 50:
                self.grade = 'C+'
            else:
                self.grade = 'C'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} | {self.exam.subject.name} | Score: {self.score} | Grade: {self.grade} | {self.percentage:.2f}%"


# Custom user model for customers
class Customer(DateTimeModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.email
