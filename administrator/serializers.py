from Users.models import Courses, Instructor, Administrator, Student, Year
from rest_framework import serializers

# Function to retrieve the list of instructors for the current user
def get_available_instructors(user):
    school_object = Administrator.objects.get(user=user)
    available_instructors = list(Instructor.objects.filter(school=school_object).values_list('name'))
    return available_instructors

# function to retrieve available classrooms in the school
def get_available_year(user):
    school_object = Administrator.objects.get(user=user)
    available_year = list(Year.objects.filter(school=school_object).values('name'))
    list_of_years = []
    for school in available_year:
        list_of_years.append(school['name'])
    return list_of_years
    

#Serializer for creating courses
class CreateCourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.ChoiceField(choices=[])
    year_name = serializers.ChoiceField(choices=[])

    class Meta:
        model = Courses
        fields = ['title', 'year_name', 'instructor_name', 'credit']
        extra_kwargs = {
            'title': {'required': True},
            'credit': {'required': True},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_dynamic_choices()

    def set_dynamic_choices(self):
        user = self.context["request"].user
        self.fields["year_name"].choices = get_available_year(user)
        available_instructors = get_available_instructors(user)
        self.fields["instructor_name"].choices = [(name, name) for name in available_instructors]

    def save(self, **kwargs):
        school_object = Administrator.objects.get(user=self.context["request"].user)
        year_name = self.validated_data['year_name']
        instructor_name = self.validated_data['instructor_name']
        year_object = Year.objects.get(name=year_name, school=school_object)
        instructor_object = Instructor.objects.get(name=instructor_name, school=school_object)
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
        fields = '__all__'
        
#Serializers for classroom 
class ClassroomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Year
        fields = ['name', 'year']
        
#Serializer to list all the students of a class
class ListAllStudentInClassSerializer(serializers.ModelSerializer):
    student_in_class = StudentSerializer(many=True, source='student_set')
    class Meta:
        model = Year
        fields = ['name', 'student_in_class']
        
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