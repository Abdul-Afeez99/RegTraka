from rest_framework import serializers
from rest_framework.fields import empty
from .models import CustomUser, Administrator, Instructor, Courses, Student, Year
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login


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
  
    class Meta:
        model = Student
        fields = '__all__'
