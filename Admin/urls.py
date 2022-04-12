from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("signin/",views.signin, name="signin"),
    path("login/", views.login_page, name='login'),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("student_registration/", views.student_registration, name="student_registration"),
    path("Student_login/", views.Student_login, name="student_login"),
    path("student_view/", views.student_view, name="student_view"),
    path("student_list/", views.student_list, name="student_list"),
    path("add_book/",views.add_book,name="add_book"),
    path("", views.Index),
    path("profile/", views.Profile, name='profile'),
    path("edit_profile/", views.edit_profile, name='edit_profile'),
    path("all_books/", views.all_books, name='all_books'),
    path("issue_book/", views.issue_book, name='issue_book'),
    path("issue_booklist/", views.issue_booklist, name='issue_booklist'),
    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
    path("delete_issue/<int:myid>/", views.delete_issue, name="delete_issue"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_view/", views.student_view, name="student_view"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
