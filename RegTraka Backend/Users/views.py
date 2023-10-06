from django.shortcuts import render
from rest_framework import generics, permissions, response, status, viewsets
from .serializers import (AdministratorRegistrationSerializer, AdministratorSerializer,
                          LoginSerializer, StudentRegistrationSerializer, ClassSerializer)
from administrator.serializers import CourseSerializer
from .models import CustomUser, Administrator, Instructor, Year, Courses
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

#Admin user registration view
class AdministratorRegistrationView(generics.GenericAPIView):
    serializer_class = AdministratorRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return response.Response(
            user_data, status=status.HTTP_201_CREATED
        )

#Get all schools view
class GetAllSchoolsView(generics.ListAPIView):
    serializer_class = AdministratorSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Administrator.objects.all()
        
#Get the available classes in a school view
class ClassroomListAPIView(generics.RetrieveAPIView):
    serializer_class = ClassSerializer
    queryset = Year.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'school'
    
    def get(self, request, school):
        administrator = Administrator.objects.filter(name=school)
        classrooms = self.queryset.filter(school=administrator)
        result = []
        for classroom in classrooms:
            output = {}
            output['name'] = classroom.name
            result.append(output)
        return response.Response(result)
    
# View to get all the courses in the class 
class ListAllCoursesAPIView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_fields = ('school', 'classroom',)
    @extend_schema(
        parameters=[
            OpenApiParameter(name='school', description='Filter by school name', required=True, type=str),
            OpenApiParameter(name='classroom', description='Filter by classroom', required=True, type=str)
        ],
    )
    
    def get(self, request, *args, **kwargs):
        school = self.kwargs['school']  # Extract course title from URL
        classroom = self.kwargs['classroom']
        school_object = Administrator.objects.filter(name=school)
        classroom_object = Year.objects.filter(name=classroom)
        all_courses = self.queryset.filter(school=school_object, year=classroom_object)
        available_courses = {}
        result = []
        for course in all_courses:
            result.append(course.title)
        available_courses['courses'] = result
        return response.Response(available_courses)

#Login View for users    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
         
        if valid:
            email=serializer.data['email']
            user = CustomUser.objects.get(email=email)
            if list(CustomUser.objects.filter(email=email).values('is_administrator'))[0]['is_administrator']:
                role = "administrator"
                name = list(Administrator.objects.filter(user=user).values('name'))[0]['name']
            else:
                role = "instructor"
                name = list(Instructor.objects.filter(user=user).values('name'))[0]['name']
    
            status_code = status.HTTP_200_OK

            output = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'name': name,
                'email': serializer.data['email'],
                'role' : role   
            }
            return response.Response(output)
        
class StudentRegistrationView(viewsets.ModelViewSet):
    # queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [permissions.AllowAny]
