from Users.models import Courses, Student, Attendance, Year
from rest_framework import serializers

class StudentInClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'matric_no', 'gender']
        
    
#Serializer for creating courses
class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['title', 'year', 'credit']
        extra_kwargs = {
            'title': {'required': True},
            'credit': {'required': True},
        }

class ClassSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Year
        fields = ['name']        

class AllCourseStudentSerializer(serializers.ModelSerializer):
    student_courses = StudentInClassSerializer(many=True)
    class Meta:
        model = Courses
        fields = ['title', 'student_courses']
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'