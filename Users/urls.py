from django.urls import path
from .views import (AdministratorRegistrationView, LoginView,
                    StudentRegistrationView, GetAllSchoolsView, ClassroomListAPIView)

urlpatterns = [
    path('administrator/sign_up', AdministratorRegistrationView.as_view(), name="administrator_registration"),
    path('user/sign_in', LoginView.as_view(), name="User_login"),
    path('student/registration', StudentRegistrationView.as_view({'post': 'create'}), name="student_registration"),
    path('get_available_schools', GetAllSchoolsView.as_view(), name="All_available_schools"),
    path('classes_in_school/<str:school>', ClassroomListAPIView.as_view(), name="All_classes_in_school")
]