from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import TemplateView,View,CreateView,FormView
from .forms import *
from .models import *
from django.http import Http404, JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate, logout

#For Mixin
class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('smsapp:customer_login'))  # Redirects to login page if not authenticated
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
    


#User Register direct login 
class CustomerRegisterView(CreateView):
    template_name ="signup.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("smsapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


#For Customer Logout
class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("smsapp:home")


#For Customer Login
class CustomerLoginView(FormView):
    template_name ="login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("smsapp:home")
    # form_valid method is a type of post method and is available in CreateView FormView and updateview.
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self. success_url



class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')  # Get search query from input

        # Perform a case-insensitive search
        results = Student.objects.filter(name__icontains=query) if query else []

        # Find related products (e.g., in the same category as the first result)
        related_products = []
        if results:
            first_product = results.first()  # Get the first product from results
            related_products = Student.objects.filter(
                category=first_product.category
            ).exclude(id=first_product.id)

        # Add results and related products to the context
        context['query'] = query
        context['results'] = results
        context['related_products'] = related_products
        return context
    

 
class HomeView(TemplateView):
    template_name = 'home.html'



class StaffCreateView(TemplateView):
    template_name = "staff/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = StaffForm()
        return context

    def post(self, request, *args, **kwargs):
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Staff created successfully.")
                return redirect('smsapp:staff_create')
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {str(e)}")
        else:
            messages.error(request, "The form is invalid.")
        return render(request, self.template_name, {'form': form})


class StaffListView(TemplateView):
    template_name = 'staff/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            staff_queryset = Staff.objects.all()  # Fetch all staff records
            paginator = Paginator(staff_queryset, 2)  # Paginate, 2 staff per page
            page_number = self.request.GET.get('page', 1)  # Default to the first page

            try:
                staff_data = paginator.page(page_number)
            except PageNotAnInteger:
                staff_data = paginator.page(1)  # Load the first page if the page is not an integer
            except EmptyPage:
                staff_data = paginator.page(paginator.num_pages)  # Load the last page if the page exceeds limits

            context['staff_list'] = staff_data  # Paginated staff list
            context['lastpage'] = paginator.num_pages  # Total number of pages
            context['totalpagelist'] = range(1, paginator.num_pages + 1)  # List of page numbers

        except Staff.DoesNotExist:
            context['staff_list'] = None
            context['error'] = "No staff found."
        except Exception as e:
            context['staff_list'] = None
            context['error'] = f"An error occurred: {str(e)}"

        return context
    

class StaffUpdateView(TemplateView):
    template_name = "staff/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_id = self.kwargs.get('id')
        staff = Staff.objects.get(id=staff_id)
        context['forms'] = StaffForm(instance=staff)

        return context

    def post(self, request, *args, **kwargs):
        staff_id = self.kwargs.get('id')
        staff_obj = Staff.objects.get(id=staff_id)
        staff_form = StaffForm(request.POST, request.FILES, instance=staff_obj)
        if staff_form.is_valid():
            staff_form.save()
            return redirect('smsapp:staff_list')
        else:
            return render(request, self.template_name, {'forms': staff_form, 'errors_message': 'sorry!!!Not valid'})
        

class StaffDeleteView(TemplateView):
    template_name = "staff/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        staff_id = self.kwargs.get('id')

        try:
            context['staff_delete'] = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            raise Http404("staff does not exist")
        return context

    def post(self, request, *args, **kwargs):
        staff_id = self.kwargs.get('id')
        try:
            staff_delete = Staff.objects.get(id=staff_id)
            staff_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("staff does not exist")
        return redirect('smsapp:staff_list')


class StaffDetailView(TemplateView):
    template_name = "staff/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_id = self.kwargs.get('id')
        staff_obj = Staff.objects.get(id=staff_id)
        context['staff_detail'] = staff_obj

        return context


#For Grade
class GradeCreateView(TemplateView):
    template_name = "grade/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = GradeForm()
        return context

    def post(self, request, *args, **kwargs):
        form = GradeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "grade created successfully.")
                return redirect('smsapp:grade_create')
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {str(e)}")
        else:
            messages.error(request, "The form is invalid.")
        return render(request, self.template_name, {'form': form})



class GradeListView(TemplateView):
    template_name = 'grade/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Fetch all grade records
            grade_queryset = Grade.objects.all()
            
            # Paginate with 4 items per page
            paginator = Paginator(grade_queryset, 4)
            
            # Get the current page number, default to 1 if not provided
            page_number = self.request.GET.get('page', 1)

            try:
                # Fetch the appropriate page
                grade_data = paginator.page(page_number)
            except PageNotAnInteger:
                # If the page is not an integer, load the first page
                grade_data = paginator.page(1)
            except EmptyPage:
                # If the page exceeds the limit, load the last page
                grade_data = paginator.page(paginator.num_pages)

            # Pass paginated data to the template
            context['grade_list'] = grade_data
            context['totalpagelist'] = paginator.page_range  # Range of all pages
            context['lastpage'] = paginator.num_pages  # Total number of pages

        except Grade.DoesNotExist:
            # Handle the case where no grades are found
            context['grade_list'] = None
            context['error'] = "No grades found."
        except Exception as e:
            # Handle other unexpected errors
            context['grade_list'] = None
            context['error'] = f"An error occurred: {str(e)}"

        return context


#For Subject

class SubjectCreateView(TemplateView):
    template_name = "subject/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubjectForm()  # Pass 'form' to the template, not 'forms'
        return context

    def post(self, request, *args, **kwargs):
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()  # Save the subject form
                messages.success(request, "Subject created successfully.")
                return redirect('smsapp:subject_create')  # Redirect to subject list
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {str(e)}")
        else:
            messages.error(request, "The form is invalid.")
        
        # In case of invalid form, render the template again with the form
        return render(request, self.template_name, {'form': form})  # 'form' instead of 'forms'



class SubjectListView(TemplateView):
    template_name = 'subject/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            subject_queryset = Subject.objects.all()  # Fetch all staff records
            paginator = Paginator(subject_queryset, 4)  # Paginate, 2 staff per page
            page_number = self.request.GET.get('page', 1)  # Default to the first page

            try:
                subject_data = paginator.page(page_number)
            except PageNotAnInteger:
                subject_data = paginator.page(1)  # Load the first page if the page is not an integer
            except EmptyPage:
                subject_data = paginator.page(paginator.num_pages)  # Load the last page if the page exceeds limits

            context['subject_list'] = subject_data  # Paginated staff list
            context['lastpage'] = paginator.num_pages  # Total number of pages
            context['totalpagelist'] = range(1, paginator.num_pages + 1)  # List of page numbers

        except Subject.DoesNotExist:
            context['subject_list'] = None
            context['error'] = "No subject found."
        except Exception as e:
            context['subject_list'] = None
            context['error'] = f"An error occurred: {str(e)}"

        return context
    

class SubjectUpdateView(TemplateView):
    template_name = "subject/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_id = self.kwargs.get('id')
        subject = Subject.objects.get(id=subject_id)
        context['form'] = SubjectForm(instance=subject)

        return context

    def post(self, request, *args, **kwargs):
        subject_id = self.kwargs.get('id')
        subject_obj = Subject.objects.get(id=subject_id)
        subject_form = SubjectForm(request.POST, request.FILES, instance=subject_obj)
        if subject_form.is_valid():
            subject_form.save()
            return redirect('smsapp:subject_list')
        else:
            return render(request, self.template_name, {'form': subject_form, 'errors_message': 'sorry!!!Not valid'})
        

class SubjectDeleteView(TemplateView):
    template_name = "subject/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('id')

        try:
            context['subject_delete'] = Subject.objects.get(id=student_id)
        except Subject.DoesNotExist:
            raise Http404("subject does not exist")
        return context

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('id')
        try:
            subject_delete = Subject.objects.get(id=product_id)
            subject_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("subject does not exist")
        return redirect('smsapp:subject_list')


#For Student
class StudentCreateView(TemplateView):
    template_name = "student/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StudentForm()  # Use 'form' consistently
        return context

    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()  # Save the form instance
                messages.success(request, "Student created successfully.")
                return redirect('smsapp:student_create')  # Ensure this URL exists in urls.py
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {str(e)}")
        else:
            messages.error(request, "The form is invalid.")
        
        # Re-render the template with the invalid form
        return render(request, self.template_name, {'form': form})
    

class StudentListView(TemplateView):
    template_name = 'student/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student_queryset = Student.objects.all()  # Fetch all student records
            paginator = Paginator(student_queryset, 4)  # Paginate, 4 students per page
            page_number = self.request.GET.get('page', 1)  # Default to the first page

            try:
                student_data = paginator.page(page_number)
            except PageNotAnInteger:
                student_data = paginator.page(1)  # Load the first page if page is not an integer
            except EmptyPage:
                student_data = paginator.page(paginator.num_pages)  # Load the last page if page exceeds limits

            context['student_list'] = student_data  # Paginated student list
            context['lastpage'] = paginator.num_pages  # Total number of pages
            context['totalpagelist'] = range(1, paginator.num_pages + 1)  # List of page numbers

        except Student.DoesNotExist:  # Correct model exception
            context['student_list'] = None
            context['error'] = "No student found."
        except Exception as e:
            context['student_list'] = None  # Correct key in context
            context['error'] = f"An error occurred: {str(e)}"

        return context
    
class StudentUpdateView(TemplateView):
    template_name = "student/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('id')
        student = Student.objects.get(id=student_id)
        context['form'] = StudentForm(instance=student)

        return context

    def post(self, request, *args, **kwargs):
        student_id = self.kwargs.get('id')
        student_obj = Student.objects.get(id=student_id)
        student_form = StudentForm(request.POST, request.FILES, instance=student_obj)
        if student_form.is_valid():
            student_form.save()
            return redirect('smsapp:student_list')
        else:
            return render(request, self.template_name, {'form': student_form, 'errors_message': 'sorry!!!Not valid'})
        

class StudentDeleteView(TemplateView):
    template_name = "student/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('id')

        try:
            context['student_delete'] = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise Http404("student does not exist")
        return context

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('id')
        try:
            student_delete = Student.objects.get(id=product_id)
            student_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("student does not exist")
        return redirect('smsapp:student_list')



class StudentDetailView(TemplateView):
    template_name = "student/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('id')
        detail_obj = Student.objects.get(id=student_id)

        exam_obj = Exam.objects.get(id=student_id)

        context['exam_detail'] = exam_obj
        context['student_detail'] = detail_obj

        return context



#For Books
class BooksListView(TemplateView):
    template_name = 'books/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            books_queryset = Book.objects.all().order_by('id')  # Order the queryset
            paginator = Paginator(books_queryset, 2)  # Paginate, 2 books per page
            page_number = self.request.GET.get('page', 1)  # Default to the first page

            try:
                books_data = paginator.page(page_number)
            except PageNotAnInteger:
                books_data = paginator.page(1)  # Load the first page if the page is not an integer
            except EmptyPage:
                books_data = paginator.page(paginator.num_pages)  # Load the last page if the page exceeds limits

            context['books_list'] = books_data  # Paginated book list
            context['last_page'] = paginator.num_pages  # Total number of pages
            context['total_page_list'] = range(1, paginator.num_pages + 1)  # List of page numbers

        except Book.DoesNotExist:
            context['books_list'] = None
            context['error'] = "No books found."
        except Exception as e:
            context['books_list'] = None
            context['error'] = f"An error occurred: {str(e)}"

        return context


class BooksCreateView(TemplateView):
    template_name = "books/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookForm()
        return context

    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Book created successfully.")
                return redirect('smsapp:books_list')
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {str(e)}")
        else:
            # Log form errors to help debug
            print("Form errors:", form.errors)
            messages.error(request, "The form is invalid. Please check the fields.")

        # Render the form with errors
        return self.render_to_response({'form': form})


class BooksUpdateView(TemplateView):
    template_name = "books/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        books_id = self.kwargs.get('id')
        books = Book.objects.get(id=books_id)
        context['form'] = BookForm(instance=books)

        return context

    def post(self, request, *args, **kwargs):
        books_id = self.kwargs.get('id')
        books_obj = Book.objects.get(id=books_id)
        books_form = BookForm(request.POST, request.FILES, instance=books_obj)
        if books_form.is_valid():
            books_form.save()
            return redirect('smsapp:books_list')
        else:
            return render(request, self.template_name, {'form': books_form, 'errors_message': 'sorry!!!Not valid'})
        

class BooksDeleteView(TemplateView):
    template_name = "books/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        books_id = self.kwargs.get('id')

        try:
            context['books_delete'] = Book.objects.get(id=books_id)
        except Book.DoesNotExist:
            raise Http404("book does not exist")
        return context

    def post(self, request, *args, **kwargs):
        books_id = self.kwargs.get('id')
        try:
            books_delete = Book.objects.get(id=books_id)
            books_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("book does not exist")
        return redirect('smsapp:books_list')



class BooksDetailView(TemplateView):
    template_name = "books/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books_id = self.kwargs.get('id')
        books = Book.objects.get(id=books_id)
        context['books_detail'] = books

        return context


#For Attendance
class AttendanceListView(TemplateView):
    template_name = 'attendance/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Order the queryset for consistent pagination
            attendance_queryset = Attendance.objects.all().order_by('id')
            paginator = Paginator(attendance_queryset, 4)  # Paginate, 4 records per page
            page_number = self.request.GET.get('page', 1)  # Default to the first page

            try:
                attendance_data = paginator.page(page_number)
            except PageNotAnInteger:
                attendance_data = paginator.page(1)  # Load the first page if invalid
            except EmptyPage:
                attendance_data = paginator.page(paginator.num_pages)  # Load the last page if out of range

            context['attendance_list'] = attendance_data
            context['lastpage'] = paginator.num_pages
            context['totalpagelist'] = range(1, paginator.num_pages + 1)

        except Attendance.DoesNotExist:
            context['attendance_list'] = None
            context['error'] = "No Attendance found."
        except Exception as e:
            context['attendance_list'] = None
            context['error'] = f"An error occurred: {str(e)}"

        return context



class AttendanceCreateView(TemplateView):
    template_name = "attendance/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AttendanceForm()
        return context

    def post(self, request, *args, **kwargs):
        form = AttendanceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Attendance created successfully.")
            return redirect('smsapp:attendance_list')  # Adjust the redirect URL as needed
        else:
            messages.error(request, "Error creating attendance.")
            return render(request, self.template_name, {'form': form})


class AttendanceUpdateView(TemplateView):
    template_name = "attendance/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        atten_id = self.kwargs.get('id')
        attendance = Attendance.objects.get(id=atten_id)
        context['form'] = AttendanceForm(instance=attendance)

        return context

    def post(self, request, *args, **kwargs):
        atten_id = self.kwargs.get('id')
        attend_obj = Attendance.objects.get(id=atten_id)
        attendance_form = AttendanceForm(request.POST, request.FILES, instance=attend_obj)
        if attendance_form.is_valid():
            attendance_form.save()
            return redirect('smsapp:attendance_list')
        else:
            return render(request, self.template_name, {'form': attendance_form, 'errors_message': 'sorry!!!Not valid'})
        

class AttendanceDeleteView(TemplateView):
    template_name = "attendance/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        attendance_id = self.kwargs.get('id')

        try:
            context['attendance_delete'] = Attendance.objects.get(id=attendance_id)
        except Attendance.DoesNotExist:
            raise Http404("attendance does not exist")
        return context

    def post(self, request, *args, **kwargs):
        atten_id = self.kwargs.get('id')
        try:
            attendance_delete = Attendance.objects.get(id=atten_id)
            attendance_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("attendance does not exist")
        return redirect('smsapp:attendance_list')



#For Exam
class ExamListView(TemplateView):
    template_name = 'exam/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch all exam records
        exam_queryset = Exam.objects.all()
        
        # Paginate exams, 4 exams per page
        paginator = Paginator(exam_queryset, 4)
        page_number = self.request.GET.get('page', 1)
        
        # Handle pagination
        exam_data = paginator.get_page(page_number)  # Returns a page object
        
        # Populate context
        context['exam_list'] = exam_data
        context['total_page_list'] = range(1, paginator.num_pages + 1)
        context['last_page'] = paginator.num_pages
        
        return context



class ExamCreateView(TemplateView):
    template_name = "exam/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExamForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Exam created successfully.")
                return redirect('smsapp:exam_list')
            except Exception as e:
                print(f"Exception occurred: {e}")
                messages.error(request, f"An error occurred: {e}")
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, "Form submission failed.")
        return render(request, self.template_name, {'form': form})
    


class ExamUpdateView(TemplateView):
    template_name = "exam/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_id = self.kwargs.get('id')
        exams = Exam.objects.get(id=exam_id)
        context['form'] = ExamForm(instance=exams)

        return context

    def post(self, request, *args, **kwargs):
        exam_id = self.kwargs.get('id')
        exam_obj = Exam.objects.get(id=exam_id)
        exam_form = ExamForm(request.POST, request.FILES, instance=exam_obj)
        if exam_form.is_valid():
            exam_form.save()
            return redirect('smsapp:exam_list')
        else:
            return render(request, self.template_name, {'form': exam_form, 'errors_message': 'sorry!!!Not valid'})
        

class ExamDeleteView(TemplateView):
    template_name = "exam/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        exam_id = self.kwargs.get('id')

        try:
            context['exam_delete'] = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            raise Http404("exam does not exist")
        return context

    def post(self, request, *args, **kwargs):
        exam_id = self.kwargs.get('id')
        try:
            exam_delete = Book.objects.get(id=exam_id)
            exam_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("exam does not exist")
        return redirect('smsapp:exam_list')



class ExamDetailView(TemplateView):
    template_name = "exam/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_id = self.kwargs.get('id')
        exam = Exam.objects.get(id=exam_id)
        context['exam_detail'] = exam

        return context


#For Result
class ResultListView(TemplateView):
    template_name = 'result/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result_queryset = Result.objects.all().order_by('-id')  # Fetch all results

        # Pagination setup: 4 results per page
        paginator = Paginator(result_queryset, 4)
        page_number = self.request.GET.get('page', 1)

        try:
            result_data = paginator.page(page_number)
        except PageNotAnInteger:
            result_data = paginator.page(1)  # Default to the first page
        except EmptyPage:
            result_data = paginator.page(paginator.num_pages)  # Show last page on out-of-range

        # Add paginated results to context
        context.update({
            'result_list': result_data,  # Paginated results
            'total_pages': paginator.num_pages,  # Total pages
            'page_range': paginator.page_range,  # Range of pages
        })
        return context


class ResultCreateView(CreateView):
    model = Result
    form_class = ResultForm
    template_name = "result/create.html"
    success_url = reverse_lazy('smsapp:result_list')  # Redirect to the result list page after successful creation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()  # Fetch all students for dropdown
        context['subjects'] = Subject.objects.all()  # Fetch all subjects for dropdown
        context['exam_types'] = Exam.objects.values_list('id', 'exam_type')  # Fetch exam types
        return context

class ResultUpdateView(TemplateView):
    template_name = "result/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        result_id = self.kwargs.get('id')
        result = Result.objects.get(id=result_id)
        context['form'] = ResultForm(instance=result)

        return context

    def post(self, request, *args, **kwargs):
        result_id = self.kwargs.get('id')
        result_obj = Result.objects.get(id=result_id)
        result_form = ResultForm(request.POST, request.FILES, instance=result_obj)
        if result_form.is_valid():
            result_form.save()
            return redirect('smsapp:result_list')
        else:
            return render(request, self.template_name, {'form': result_form, 'errors_message': 'sorry!!!Not valid'})
        

class ResultDeleteView(TemplateView):
    template_name = "result/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        result_id = self.kwargs.get('id')

        try:
            context['result_delete'] = Result.objects.get(id=result_id)
        except Result.DoesNotExist:
            raise Http404("result does not exist")
        return context

    def post(self, request, *args, **kwargs):
        result_id = self.kwargs.get('id')
        try:
            result_delete = Book.objects.get(id=result_id)
            result_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("result does not exist")
        return redirect('smsapp:result_list')



class ResultDetailView(TemplateView):
    template_name = "result/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result_id = self.kwargs.get('id')
        result = Result.objects.get(id=result_id)
        context['result_detail'] = result

        return context

