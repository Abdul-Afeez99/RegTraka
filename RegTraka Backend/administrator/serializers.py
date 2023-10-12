from Users.models import Courses, Instructor, Administrator, Student, Year
from rest_framework import serializers

    
#Serializer for creating courses
class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['title', 'year', 'instructor', 'credit']
        extra_kwargs = {
            'title': {'required': True},
            'credit': {'required': True},
        }


    def save(self, **kwargs):
        school_object = Administrator.objects.get(user=self.context["request"].user)
        year= self.validated_data['year']
        instructor = self.validated_data['instructor']
        year_object = Year.objects.get(name=year, school=school_object)
        instructor_object = Instructor.objects.get(name=instructor, school=school_object)
        Courses.objects.create(
            title=self.validated_data['title'],
            year=year_object,
            credit=self.validated_data['credit'],
            instructor=instructor_object,
            school=school_object,
        )
        
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
