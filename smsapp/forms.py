from django import forms
from .models import *


# Login Form
class CustomerLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


# User Form
class CustomerRegistrationForm(forms.ModelForm):
    username= forms.CharField(widget=forms.TextInput())
    password= forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = Customer
        fields = [ "username", "password", "email",]
    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Customer with this username already exists.")
        return uname
    

# Grade Form
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Name"
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Description"
            }),
        }


# Subject Form
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Name"
            }),
            'grade': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Description"
            }),
        }


# Teacher Form
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'name', 'role', 'subject', 'phone', 'email', 'address', 'date_of_birth',
            'hire_date', 'profile_picture', 'is_active', 'qualifications'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Name"
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Phone Number"
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "Email"
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Address"
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'hire_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'qualifications': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Qualifications"
            }),
        }

# Book Form
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'subject', 'grade', 'isbn', 'publication_date',
            'publisher', 'page_count', 'language', 'available_copies'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Title"
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
            }),
            'grade': forms.Select(attrs={
                'class': 'form-control',
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "ISBN"
            }),
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Publisher"
            }),
            'page_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Page Count"
            }),
            'language': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Language"
            }),
            'available_copies': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Available Copies"
            }),
        }

# Student Form
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'roll_number', 'grade', 'date_of_birth', 'gender', 'email',
            'phone', 'address', 'admission_date', 'profile_picture', 'parent_name',
            'parent_contact', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Name"
            }),
            'roll_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'grade': forms.Select(attrs={
                'class': 'form-control',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "Email"
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Phone"
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Address"
            }),
            'admission_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'parent_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Parent's Name"
            }),
            'parent_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Parent's Contact"
            }),
        }

# Attendance Form
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['role', 'student', 'staff', 'date', 'status', 'check_in_time', 'check_out_time']
        widgets = {
            'check_in_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        student = cleaned_data.get('student')
        staff = cleaned_data.get('staff')

        # Ensure the role matches the selected person
        if role == 'Student' and not student:
            raise forms.ValidationError("Student must be selected for role 'Student'.")
        if role == 'Staff' and not staff:
            raise forms.ValidationError("Staff must be selected for role 'Staff'.")
        if role == 'Student' and staff:
            raise forms.ValidationError("Staff should not be selected when role is 'Student'.")
        if role == 'Staff' and student:
            raise forms.ValidationError("Student should not be selected when role is 'Staff'.")

        # Check if check-in time is earlier than check-out time
        check_in_time = cleaned_data.get('check_in_time')
        check_out_time = cleaned_data.get('check_out_time')
        if check_in_time and check_out_time and check_in_time >= check_out_time:
            raise forms.ValidationError("Check-in time must be earlier than check-out time.")

        return cleaned_data

    
# Exam Form

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'date', 'exam_type', 'grade', 'duration', 'description']
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-control',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'exam_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'grade': forms.Select(attrs={
                'class': 'form-control',
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Duration (in hours)"
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Description"
            }),
        }

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration is None or duration <= 0:
            raise forms.ValidationError("Duration must be a positive number.")
        return duration



# Result Form

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'exam','date', 'grade', 'score', 'total_marks',]
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control',
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
            }),
            'exam': forms.Select(attrs={
                'class': 'form-control',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter result"
            }),
            'grade': forms.Select(attrs={
                'class': 'form-control',
            }),
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Score"
            }),

            'total_marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Total Marks"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        score = cleaned_data.get('score')
        total_marks = cleaned_data.get('total_marks')

        # Validation to ensure score is not greater than total marks
        if score and total_marks and score > total_marks:
            raise forms.ValidationError("Score cannot be greater than total marks.")

        return cleaned_data
