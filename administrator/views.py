from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, GenericAPIView
from .serializers import (CourseSerializer, InstructorSerializer, ClassroomSerializer, StudentSerializer, CreateCourseSerializer,
                          ListAllStudentInClassSerializer, IndividualInstructorSerializer, CreateClassroomSerializer)
from Users.models import Courses, Administrator, Instructor, Year, Student
from rest_framework import permissions, response, status
from Users.permissions import IsAdministrator
from Users.serializers import UserSerializer
from Users.serializers import InstructorRegistrationSerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

# get the administrator object
def getAdministratorObject(self,):
    user_obj = self.request.user
    school = Administrator.objects.get(user=user_obj)
    return school


# Get the current instructor information
class AdministratorInfoView(RetrieveAPIView):
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        administrator = Administrator.objects.filter(user=user)
        result = {}
        for info in administrator:
            result['name'] = info.name
            result['email'] = info.user.email
        return response.Response(result, status=status.HTTP_200_OK)

#create a new instructor
class InstructorRegistrationView(GenericAPIView):
    serializer_class = InstructorRegistrationSerializer
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "Instructor registration",
        operation_description= "Returns the instructor information"
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        return response.Response(
            user_data, status=status.HTTP_201_CREATED
        )   
    
# Create a new course   
class CourseCreateAPIView(CreateAPIView):
    serializer_class = CreateCourseSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "Create a new course",
        operation_description= "Create a new course and add it to the list of available courses."
    )
    def perform_create(self, serializer):
        school = getAdministratorObject(self)
        return serializer.save(school=school)

# list all courses available in the school  
class CourseListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "List courses in school",
        operation_description= "Returns list of courses in school"
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        courses = self.queryset.filter(school=school)
        result = []
        for course in courses:
            output = {
                'title': course.title,
                'credit': course.credit,
                'instructor': course.instructor.name,
                'class' : course.year.name
            }
            result.append(output)
        return response.Response(result, status=status.HTTP_200_OK)
    
#Get total number of courses in a school
class TotalCoursesInSchoolAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "Get total number of courses in school",
        operation_description= "Returns total number of courses in the school"
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        total_courses = self.queryset.filter(school=school).count()
        result = {"Total_Course": total_courses}
        return response.Response(result)
    
# Modify an individual course 
class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsAdministrator,permissions.IsAuthenticated]
    lookup_field = "title"
    
    def perform_create(self, serializer):
        school = getAdministratorObject(self)
        return serializer.save(school=school)
    
    @swagger_auto_schema(
        operation_summary = "Get a particular course",
        operation_description= "Returns course details"
    )
    def get(self, request, title):
        course = self.queryset.filter(school=getAdministratorObject(self), title=title)
        result = []
        for info in course:
            output = {}
            output['title'] = info.title
            output['class'] = info.year.name
            output['instructor'] = info.instructor.name
            output['credit'] = info.credit
            result.append(output)
        return response.Response(result)
    
    
            
# List all instructors in the school
class InsructorListAPIView(ListAPIView):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "List instructors in school",
        operation_description= "Returns list of instructors in school"
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        instructors = self.queryset.filter(school=school)
        result = []
        for instructor in instructors:
            output = {}
            output['name'] = instructor.name
            output['gender'] = instructor.gender
            result.append(output)
        return response.Response(result)
    
#Get total number of instructors in a school
class TotalInstructorsInSchoolAPIView(ListAPIView):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "Get total number of instructors in school",
        operation_description= "Returns total number of instructors in the school"
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        total_instructors = self.queryset.filter(school=school).count()
        result = {"Total_Instructors": total_instructors}
        return response.Response(result)

# Modify individual Instructor
class InsructorModifyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = IndividualInstructorSerializer
    queryset = Instructor.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    lookup_field = "name"
    
    @swagger_auto_schema(
        operation_summary = "Get a particular instructor in school",
        operation_description= "Returns instructor detail"
    )
    def get(self, request, name):
        school = getAdministratorObject(self)
        instructors = self.queryset.filter(school=school, name=name)
        result = []
        for instructor in instructors:
            output = {}
            output['name'] = instructor.name
            output['gender'] = instructor.gender
            result.append(output)
        return response.Response(result)
    
    
    
# Create a new classroom   
class ClassroomCreateAPIView(CreateAPIView):
    serializer_class = CreateClassroomSerializer
    queryset = Year.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        school = getAdministratorObject(self)
        return serializer.save(school=school)
    
# list all classrooms available in the school  
class ClassroomListAPIView(ListAPIView):
    serializer_class = ClassroomSerializer
    queryset = Year.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "List all classrooms in school",
        operation_description= "Returns list of classrooms in school"
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        classrooms = self.queryset.filter(school=school)
        result = []
        for classroom in classrooms:
            output = {}
            output['name'] = classroom.name
            output['year'] = classroom.year
            result.append(output)
        return response.Response(result)

# List all the students in a class    
class StudentListAPIView(RetrieveAPIView):
    serializer_class = ListAllStudentInClassSerializer
    queryset = Year.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    lookup_field = "year"
    
    
    @swagger_auto_schema(
        operation_summary = "List all students in a class",
        operation_description= "Returns list of students in class"
    )
    def get_queryset(self):
        school = getAdministratorObject(self)
        return self.queryset.filter(school=school)
    
#Get total number of students in a school
class TotalStudentInSchoolAPIView(ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "Get total number of students in school",
        operation_description= "Returns total number of students in the school"
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        total_students = self.queryset.filter(school=school).count()
        result = {"Total_Student": total_students}
        return response.Response(result)
    
# Get total male students in a school
class TotalMaleStudentInSchoolAPIView(ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "Get total number of male students in school",
        operation_description= "Returns total number of male students in the school"
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        total_students = self.queryset.filter(school=school, gender='Male').count()
        result = {"Total_male_student": total_students}
        return response.Response(result)
   
# Get total female students in a school
class TotalFemaleStudentInSchoolAPIView(ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary = "Get total number of female students in school",
        operation_description= "Returns total number of female students in the school"
    )
    def get(self, request, *args, **kwargs):
        school = getAdministratorObject(self)
        total_students = self.queryset.filter(school=school, gender='Female').count()
        result = {"Total_female_student": total_students}
        return response.Response(result)
        
# Modify student information
class StudentAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAdministrator&permissions.IsAuthenticated]
    lookup_field = "matric_no"
    
    def perform_create(self, serializer):
        school = getAdministratorObject(self)
        return serializer.save(school=school)
    
    @swagger_auto_schema(
        operation_summary = "Get a student information",
        operation_description= "Returns student information"
    )
    def get_queryset(self):
        school = getAdministratorObject(self)
        return list(self.queryset.filter(school=school).values())   
         
