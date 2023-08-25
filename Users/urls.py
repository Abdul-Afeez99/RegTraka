from django.urls import path
from .views import (AdministratorRegistrationView, LoginView,
                    StudentRegistrationView)

urlpatterns = [
    path('administrator/sign_up', AdministratorRegistrationView.as_view(), name="administrator_registration"),
    path('user/sign_in', LoginView.as_view(), name="User_login"),
    path('student/registration', StudentRegistrationView.as_view({'post': 'create'}), name="student_registration"),
]