from Users.models import Courses, Student, Attendance
from rest_framework import serializers

class StudentInClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'matric_no', 'gender']
        
    


class AllCourseStudentSerializer(serializers.ModelSerializer):
    student_courses = StudentInClassSerializer(many=True)
    class Meta:
        model = Courses
        fields = ['title', 'student_courses']
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'