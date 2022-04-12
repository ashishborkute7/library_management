from django.shortcuts import render
from django.shortcuts import redirect, render,HttpResponse
from .models import *
'''from .forms import IssueBookForm'''
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from . import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required

# Create your views here.
def signin(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.success(request, "Username already exist!")

            elif User.objects.filter(email=email).exists():
                messages.success(request, "Email already exist!")
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.save()
                messages.success(request, "Admin Registered Successfully")
                return render(request, "login.html")
        else:
            messages.error(request,"Password is mismatch")
    return render(request, "admin_registration.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                messages.success(request, "Admin Login Successfully")
                return redirect("/add_book")
            else:
                messages.success(request,"This Page is For Admin Access Only!")
                return redirect("/")
        else:
            return redirect("/")
    else:
        return render(request, "login.html",)
    return render(request, 'login.html')

def Student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                messages.success(request, "This Page is For Students View Access!")
                return render(request, "login.html", )
            else:
                messages.success(request, "Student Login Successfully")
                return render(request, "student_view.html", )
        else:
            return redirect("student_registration")
    else:

        return render(request, "student_login.html")
    return render(request, "student_login.html")

def Profile(request):


    return render(request,'profile.html')


@login_required(login_url = '/login')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        subject = request.POST['subject']
        category = request.POST['category']
        books = Book.objects.create(name=name, author=author, subject=subject, category=category)
        books.save()
        messages.success(request,"Book Added Successfully!")
        return render(request, "add_book1.html")
    return render(request, "add_book1.html")

@login_required(login_url = '/login')
def all_books(request):
    books = Book.objects.all()
    return render(request, "all_books.html", {'books':books})

@login_required(login_url = '/login')
def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/all_books")

@login_required(login_url = '/login')
def delete_issue(request, myid):
    issue = IssuedBook.objects.filter(id=myid)
    issue.delete()
    return redirect("/issue_booklist")


def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.success(request, "Username already exist!")

            elif User.objects.filter(email=email).exists():
                messages.success(request, "Email already exist!")
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                student = Student.objects.create(user=user, phone=phone, branch=branch, classroom=classroom,roll_no=roll_no)
                user.save()
                student.save()
                messages.success(request,"Student Registered Successfully")
                return redirect("/Student_login")
        else:
            messages.success(request, "Password is Mismatch!")

    return render(request, "student_sign.html")


@login_required(login_url = '/student_login')
def student_view(request):
    student = Student.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    li1 = []
    li2 = []

    for i in issuedBooks:
        books = Book.objects.filter(subject=i.subject)
        for book in books:
            t = (request.user.id, request.user.get_full_name, book.name, book.author)
            li1.append(t)

        days = (date.today() - i.issued_date)
        d = days.days
        fine = 0
        if d > 15:
            day = d - 15
            fine = day * 5
        t = (issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
        li2.append(t)
        return render(request, 'student_view.html', {'li1': li1, 'li2': li2})
    return render(request, 'student_view.html')



def logout_user(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect ("/")

def Index(request):

    return render(request,"index.html")


@login_required(login_url = '/login')
def student_list(request):
    students = Student.objects.all()
    return render(request, "student_list.html", {'students':students})

@login_required(login_url = '/login')
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.student_id = request.POST['name2']
            obj.subject = request.POST['subject2']
            obj.save()
            alert = True
            return render(request, "issue_books.html", {'obj':obj, 'alert':alert})
    return render(request, "issue_books.html", {'form':form})


@login_required(login_url = '/login')
def issue_booklist(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        days = (date.today() - i.issued_date)
        d = days.days
        fine = 0
        if d > 30:
            day = d - 30
            fine = day * 5
        books = list(models.Book.objects.filter(subject=i.subject))
        students = list(models.Student.objects.filter(user=i.student_id))
        i=0
        for l in books:
            t = (students[i].user, students[i].user_id, books[i].name, books[i].subject, issuedBooks[0].issued_date,issuedBooks[0].expiry_date, fine)
            i=i+1
            details.append(t)
    return render(request, "issue_booklist.html", {'issuedBooks':issuedBooks, 'details':details})


@login_required(login_url = '/login')
def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    students.delete()
    return redirect("/student_list")

@login_required(login_url = '/student_login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "password_reset.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "password_reset.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "password_reset.html")


@login_required(login_url = '/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        student.user.email = email
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no
        student.user.save()
        student.save()
        alert = True
        return render(request, "edit_profile.html", {'alert':alert})
    return render(request, "edit_profile.html")
