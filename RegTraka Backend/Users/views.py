from django.shortcuts import render
from rest_framework import generics, permissions, response, status, viewsets
from .serializers import (AdministratorRegistrationSerializer, AdministratorSerializer,
                          LoginSerializer, StudentRegistrationSerializer, ClassSerializer, UserSerializer)
from administrator.serializers import CourseSerializer
from .models import CustomUser, Administrator, Instructor, Year, Courses
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter


#Get current user view
class CurrentUserDashboardView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

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
class ClassroomListAPIView(generics.ListAPIView):
    serializer_class = ClassSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Year.objects.all()
    @extend_schema(
        parameters=[
            OpenApiParameter(name='school', description='Filter by school name', required=True, type=str),
        ],
    )
    def get(self, request, *args, **kwargs):
        school_name = self.request.query_params.get('school')
        if not school_name:
            return response.Response({"error": "School name is required."}, status=400)

        administrator = Administrator.objects.filter(name=school_name).first()
        if not administrator:
            return response.Response({"error": "Administrator not found."}, status=404)

        classrooms = Year.objects.filter(school=administrator)
        result = [{'name': classroom.name} for classroom in classrooms]
        return response.Response(result)
     
# View to get all the courses in the class 
class ListAllCoursesAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Courses.objects.all()
    @extend_schema(
        parameters=[
            OpenApiParameter(name='school', description='Filter by school name', required=True, type=str),
            OpenApiParameter(name='classroom', description='Filter by classroom', required=True, type=str)
        ],
    )
    def get(self, request, *args, **kwargs):
        school = self.request.query_params.get('school')
        classroom = self.request.query_params.get('classroom')
        
        school_object = Administrator.objects.filter(name=school).first()
        classroom_object = Year.objects.filter(name=classroom).first()

        if not (school_object and classroom_object):
            return response.Response({"error": "School or Classroom not found."}, status=400)
        
        all_courses = self.queryset.filter(school=school_object, year=classroom_object)
        
        available_courses = {
            "courses": [course.title for course in all_courses]
        }
        
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
