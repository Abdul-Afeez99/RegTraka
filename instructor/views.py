from administrator.serializers import IndividualInstructorSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions, response, status, viewsets
from Users.permissions import IsInstructor
from Users.models import Instructor, Courses
from Users.serializers import UserSerializer
from .serializers import AllCourseStudentSerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
# def getInstructorObject(self,):
#     user_obj = self.request.user
#     instructor = Cus.objects.get(user=user_obj)
#     return instructor

# Get the current instructor information
class InstructorInfoView(RetrieveAPIView):
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        instructor = Instructor.objects.filter(user=user)
        result = {}
        for info in instructor:
            result['name'] = info.name
            result['email'] = info.user.email
            result['school'] = info.school.name
            result['gender'] = info.gender
        return response.Response(result, status=status.HTTP_200_OK)
            

# Get the instructor courses
class GetInstructorCoursesAPIView(ListAPIView):
    serializer_class = IndividualInstructorSerializer
    queryset = Instructor.objects.all()
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        instructor = self.queryset.filter(user=user)
        serializer = self.serializer_class(instructor, many=True).data
        result = {}
        result['name'] = serializer[0]['name']
        result['courses'] = serializer[0]['instructor_courses']
        return response.Response(result, status=status.HTTP_200_OK)


# Get the student offering the course        
class ViewCourseStudentsAPIView(RetrieveAPIView):
    serializer_class = AllCourseStudentSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsInstructor&permissions.IsAuthenticated]
    lookup_field = "title"
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        instructor = Instructor.objects.get(user=user)
        course = self.queryset.filter(instructor=instructor)
        serializer = self.serializer_class(course, many=True).data
        result = {}
        result['title'] = serializer[0]['title']
        result['students'] = serializer[0]['student_courses']
        return response.Response(result, status=status.HTTP_200_OK)
