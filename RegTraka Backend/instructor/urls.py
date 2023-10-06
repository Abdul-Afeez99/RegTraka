from django.urls import path
from .views import (GetInstructorCoursesAPIView, InstructorInfoView,
                    ViewCourseStudentsAPIView, StartAttendanceView, StopAttendanceView,
                    GetCourseAttendanceView, GetCourseAttendanceByDateView, CountTotalAttendanceView)


urlpatterns = [
    path("current_instructor", InstructorInfoView.as_view(), name="Welcome-Instructor"),
    path("courses", GetInstructorCoursesAPIView.as_view(), name="Instructor-Courses" ),
    path("student_list/<str:title>", ViewCourseStudentsAPIView.as_view(), name="Student-in-class"),
    path("attendance/start", StartAttendanceView.as_view(), name="start_attendance"),
    path("attendance/stop", StopAttendanceView.as_view(), name="stop_attendance"),
    path("attendance/<str:course>", GetCourseAttendanceView.as_view(), name="get_course_attendance"),
    path("attendance/", GetCourseAttendanceByDateView.as_view(), name="get_course_attendance_by_date"),
    path("total_attendance/<str:course>", CountTotalAttendanceView.as_view(), name='total_attendance_count')
]