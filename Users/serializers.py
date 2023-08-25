from rest_framework import serializers
from rest_framework.fields import empty
from .models import CustomUser, Administrator, Instructor, Courses, Student, Year
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login

def get_all_schools():
        available_schools = list(CustomUser.administrator.get_queryset().values('name'))
        list_of_schools = []
        for school in available_schools:
            list_of_schools.append(school['name'])
        return list_of_schools
    
def get_all_courses(school, year):
    available_courses = list(Courses.objects.filter(school=school, year=year).values('title'))
    list_of_courses = []
    for course in available_courses:
        list_of_courses.append(course['title'])
    return list_of_courses

def get_available_year(school):
    available_year = list(Year.objects.filter(school=school).values('name'))
    list_of_years = []
    for school in available_year:
        list_of_years.append(school['name'])
    return list_of_years

sex = [
        ("MALE", "Male"),
        ("FEMALE", 'Female')
    ]
        
# serializers for to get the current user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =  [
            'id', 'email',  'is_administrator', 'is_instructor'
        ]

#serializer for administrator registration
class AdministratorRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=68, min_length=12, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
        extra_kwargs = {
            'name' : {'required': True}
        }
        
    def save(self, **kwargs):
        user = CustomUser(
            email = self.validated_data['email'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.is_administrator = True
        user.is_instructor = False
        user.save()
        # Save administrator data to the administrator table
        Administrator.objects.create(
            user = user,
            name = self.validated_data['name']
        )
        
        
#Serializer for instructor registration

class InstructorRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=68, min_length=12, write_only=True)
    gender= serializers.ChoiceField(choices=sex)
    
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'gender', 'password']
        extra_kwargs = {
            'name' : {'required': True},
            'email' : {'required': True},
            'gender' : {'required': True},
        }
        
    def save(self, **kwargs):
        user = CustomUser(
            email = self.validated_data['email'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.is_administrator = False
        user.is_instructor = True
        user.save()
        # Save instructor data to the instructor table
        school_object = Administrator.objects.get(user=self.context["request"].user)
        Instructor.objects.create(
            user = user,
            name = self.validated_data['name'],
            school = school_object,
            gender = self.validated_data['gender']
        )

# Serializer for user login        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'access', 'refresh']
        
    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        print(user)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
            }

            return validation
        except:
            raise serializers.ValidationError("Invalid login credentials")
        
# Student registration
class StudentRegistrationSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=sex)
    school = serializers.ChoiceField(choices=[])
    year = serializers.ChoiceField(choices=[])
    courses = serializers.MultipleChoiceField(choices=[])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school'].choices = get_all_schools()
    
    def validate_school(self, value):
        self.fields['year'].choices = get_available_year(value)
        return value
    
    def validate_year(self, value):
        school_id = self.initial_data.get('school')  # Get the school name from the initial data
        print(school_id)
        
        try:
            school = Administrator.objects.get(id=school_id)
        except Administrator.DoesNotExist:
            raise serializers.ValidationError("Invalid school id")  # Handle the case where the school doesn't exist
        
        year = Year.objects.get(school=school)
        courses = get_all_courses(school=school, year=year)
        self.fields['courses'].choices = courses
        return value

    class Meta:
        model = Student
        fields = [
            'name', 'school', 'matric_no', 'gender', 'year',
            'image', 'courses'
        ]
