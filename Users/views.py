from django.shortcuts import render
from rest_framework import generics, permissions, response, status, viewsets
from .serializers import (AdministratorRegistrationSerializer, AdministratorSerializer,
                          LoginSerializer, StudentRegistrationSerializer, ClassroomSerializer)
from .models import CustomUser, Administrator, Instructor, Year

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
    serializer_class = ClassroomSerializer
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
