from django.urls import path
from .views import GetInstructorCoursesAPIView, InstructorInfoView, ViewCourseStudentsAPIView


urlpatterns = [
    path("current_instructor", InstructorInfoView.as_view(), name="Welcome-Instructor"),
    path("courses", GetInstructorCoursesAPIView.as_view(), name="Instructor-Courses" ),
    path("student_list/<str:title>", ViewCourseStudentsAPIView.as_view(), name="Student-in-class")
]