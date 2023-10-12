from django.urls import path
from .views import (AdministratorRegistrationView, LoginView,
                    StudentRegistrationView, GetAllSchoolsView, ClassroomListAPIView, ListAllCoursesAPIView,
                    CurrentUserDashboardView)

urlpatterns = [
    path('get_current_user', CurrentUserDashboardView.as_view(), name="get_current_user_information"),
    path('administrator/sign_up', AdministratorRegistrationView.as_view(), name="administrator_registration"),
    path('user/sign_in', LoginView.as_view(), name="User_login"),
    path('student/registration', StudentRegistrationView.as_view({'post': 'create'}), name="student_registration"),
    path('get_available_schools', GetAllSchoolsView.as_view(), name="All_available_schools"),
    path('classes_in_school', ClassroomListAPIView.as_view(), name="All_classes_in_school"),
    path('available_course', ListAllCoursesAPIView.as_view(), name='get_class_courses')
]