from Users.models import Courses, Instructor, Administrator, Student, Year
from rest_framework import serializers

    
# #Serializer for creating courses
# class CreateCourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Courses
#         fields = ['title', 'year', 'instructor', 'credit']
#         extra_kwargs = {
#             'title': {'required': True},
#             'credit': {'required': True},
#         }

        
# Serializer for course        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ["title", "year", "instructor", "credit"]
        
#Serializer for Instructors
class InstructorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Instructor
        fields = ['name', 'gender']  

#Serializers for students       
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
# Serializer to create classroom    
class CreateClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ['name', 'year']
        
#Serializers for classroom 
class ClassroomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Year
        fields = ['name', 'year']
        
#Serializer to list all the students of a class
class ListAllStudentInClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'gender', 'matric_no']
        
class GetCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ["title", "year", "credit"]

# Serializer to get the details of a particular instructor        
class IndividualInstructorSerializer(serializers.ModelSerializer):
    instructor_courses = GetCourseSerializer(many=True)
    class Meta:
        model = Instructor
        fields = ['name', 'instructor_courses']
