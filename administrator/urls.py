from django.urls import path
from .views import (CourseListAPIView, CourseDetailAPIView, InsructorListAPIView, 
                    CourseCreateAPIView,InsructorModifyAPIView, ClassroomCreateAPIView,
                    ClassroomListAPIView, StudentListAPIView, StudentAPIView, InstructorRegistrationView)

urlpatterns = [
    path('add_instructor', InstructorRegistrationView.as_view(), name="instructor_registration"),
    path('create_course', CourseCreateAPIView.as_view(), name="Create Course"),
    path('courses', CourseListAPIView.as_view(), name="Available Courses"),
    path("course/<str:title>", CourseDetailAPIView.as_view(), name="Modify_course"),
    path('instructors', InsructorListAPIView.as_view(), name="Available_Instructors"),
    path('instructor/<str:name>', InsructorModifyAPIView.as_view(), name="Modify_instructor"),
    path('add-classroom', ClassroomCreateAPIView.as_view(), name="Create Classroom"),
    path('list-classrooms', ClassroomListAPIView.as_view(), name="List-all-classrooms"),
    path('class/<int:year>/student-list', StudentListAPIView.as_view(), name="list-students-in-class"),
    path('student/<str:matric_no>', StudentAPIView.as_view(), name="Modify Student")   
]