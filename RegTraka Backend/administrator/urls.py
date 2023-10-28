from django.urls import path
from .views import (CourseListAPIView, CourseDetailAPIView, InsructorListAPIView, 
                    InsructorModifyAPIView, ClassroomCreateAPIView,
                    ClassroomListAPIView, StudentListAPIView, StudentAPIView, InstructorRegistrationView,
                    TotalStudentInSchoolAPIView,TotalMaleStudentInSchoolAPIView, TotalFemaleStudentInSchoolAPIView,
                    TotalCoursesInSchoolAPIView, TotalInstructorsInSchoolAPIView, GetCourseAttendanceView, GetCourseAttendanceByDateView,
                    CountTotalAttendanceView
                    )

urlpatterns = [
    path('add_instructor', InstructorRegistrationView.as_view(), name="instructor_registration"),
    path('courses', CourseListAPIView.as_view(), name="Available Courses"),
    path("course/<str:title>", CourseDetailAPIView.as_view(), name="Modify_course"),
    path('instructors', InsructorListAPIView.as_view(), name="Available_Instructors"),
    path('instructor/<str:name>', InsructorModifyAPIView.as_view(), name="Modify_instructor"),
    path('add-classroom', ClassroomCreateAPIView.as_view(), name="Create Classroom"),
    path('list-classrooms', ClassroomListAPIView.as_view(), name="List-all-classrooms"),
    path('class/student-list', StudentListAPIView.as_view(), name="list-students-in-class"),
    path('student/<str:matric_no>', StudentAPIView.as_view(), name="Modify Student"),
    path('total_students', TotalStudentInSchoolAPIView.as_view(), name="Total_students"),
    path('total_male_student', TotalMaleStudentInSchoolAPIView.as_view(), name="Total_male_student"),
    path('total_female_student', TotalFemaleStudentInSchoolAPIView.as_view(), name="Total_female_student"),
    path('total_course', TotalCoursesInSchoolAPIView.as_view(), name="Total_courses"),
    path('total_instructors', TotalInstructorsInSchoolAPIView.as_view(), name="Total_instructors"), 
    path("attendance/<str:course>", GetCourseAttendanceView.as_view(), name="course_attendance"),
    path("attendance/", GetCourseAttendanceByDateView.as_view(), name="course_attendance_by_date"),
    path("total_attendance", CountTotalAttendanceView.as_view(), name='total_attendance')  
]